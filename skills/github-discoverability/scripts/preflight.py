#!/usr/bin/env python3
"""Read-only, dependency-free release hygiene checks. NOT a security certification.

No network, Git calls, project execution, or implicit writes. Findings never echo
matched credential values. Only the current selected files are examined.
Python 3.10+.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

IGNORE_DIRS = {'.git', '.local', '.release-private', 'node_modules', '.venv',
               'venv', '__pycache__', '.pytest_cache', 'dist', 'build'}
TEXT_SUFFIXES = {'.md', '.txt', '.json', '.yaml', '.yml', '.py', '.js', '.ts',
                 '.tsx', '.jsx', '.css', '.html', '.sh', '.ps1', '.toml', '.ini', '.cfg'}
MAX_BYTES = 1_000_000
MAX_FILES = 10000
TOKEN = '__REPO_FULL_NAME__'
CREDENTIALS = [
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    re.compile(r'\bgh[pousr]_[A-Za-z0-9]{30,}\b'),
    re.compile(r'\bgithub_pat_[A-Za-z0-9_]{40,}\b'),
    re.compile(r'\bAKIA[A-Z0-9]{16}\b'),
]
LINK = re.compile(r'(?<!!)\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)|!\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)')

def fenced_out(text: str) -> str:
    output: list[str] = []
    marker = ''
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            value = match.group(1)
            if not marker:
                marker = value
            elif value[0] == marker[0] and len(value) >= len(marker):
                marker = ''
            output.append('')
        else:
            output.append('' if marker else line)
    return '\n'.join(output)

def audit(root: Path) -> dict[str, Any]:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError('Target must be an existing directory.')
    findings: list[dict[str, Any]] = []
    files: list[Path] = []
    skipped = 0
    def add(level: str, rule: str, path: str, message: str, line: int | None = None) -> None:
        item: dict[str, Any] = dict(level=level, rule=rule, path=path, message=message)
        if line is not None:
            item['line'] = line
        findings.append(item)
    for base, dirs, names in os.walk(root, followlinks=False):
        parent = Path(base)
        retained = []
        for name in sorted(dirs):
            path = parent / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                add('block', 'symlink', relative, 'Directory symlink not followed; review publication scope.')
            elif name in IGNORE_DIRS:
                skipped += 1
            else:
                retained.append(name)
        dirs[:] = retained
        for name in sorted(names):
            path = parent / name
            if path.is_symlink():
                add('block', 'symlink', path.relative_to(root).as_posix(), 'File symlink not read.')
            else:
                files.append(path)
            if len(files) > MAX_FILES:
                raise ValueError('File limit exceeded; choose a smaller, explicit public snapshot.')
    relative_files = {p.relative_to(root).as_posix() for p in files}
    if 'README.md' not in relative_files:
        add('block', 'readme', 'README.md', 'Missing root README.md.')
    if not any(Path(p).name.lower() in {'license', 'license.md', 'license.txt', 'copying'}
               and '/' not in p for p in relative_files):
        add('block', 'license', 'LICENSE', 'Missing explicit root license; owner must choose/confirm rights.')
    checked = 0
    for path in files:
        rel = path.relative_to(root).as_posix()
        name = path.name.lower()
        if (name == '.env' or (name.startswith('.env.') and not name.endswith(('.example', '.sample', '.template')))
                or name in {'id_rsa', 'id_ed25519', 'credentials.json'}):
            add('block', 'sensitive-name', rel, 'Potential private configuration; do not publish without review.')
        try:
            if path.stat().st_size > MAX_BYTES:
                add('review', 'large-file', rel, 'Content skipped: file exceeds scan size limit.')
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {'LICENSE', 'COPYING', '.gitignore'} and not name.startswith('.env'):
                continue
            try:
                text = path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                add('review', 'encoding', rel, 'Non-UTF-8 content not inspected.')
                continue
        except OSError:
            add('block', 'unreadable', rel, 'Could not inspect this file.')
            continue
        checked += 1
        for number, line in enumerate(text.splitlines(), 1):
            if any(pattern.search(line) for pattern in CREDENTIALS):
                add('block', 'credential-shape', rel, 'Credential-shaped value found; matched value is redacted.', number)
        if TOKEN in text and rel in {'README.md', 'README.zh-CN.md', 'release/metadata.json'}:
            add('review', 'repository-unbound', rel, 'Bind the explicitly approved owner/repository before public upload.')
        if path.name == 'SKILL.md':
            chunks = text.split('---', 2)
            if not text.startswith('---\n') or len(chunks) < 3:
                add('block', 'skill-frontmatter', rel, 'Missing delimited frontmatter.')
            else:
                front = chunks[1]
                nm = re.search(r'^name:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$', front, re.M)
                ds = re.search(r'^description:\s*(\S.*)$', front, re.M)
                if not nm or len(nm.group(1)) > 64 or nm.group(1) != path.parent.name:
                    add('block', 'skill-name', rel, 'Name must match directory and use standard lowercase/hyphen form.')
                if not ds:
                    add('block', 'skill-description', rel, 'Missing description.')
                elif ds.group(1) not in {'>', '|', '>-', '|-'} and len(ds.group(1)) > 1024:
                    add('block', 'skill-description', rel, 'Inline description exceeds standard length.')
        if path.suffix.lower() == '.md':
            for match in LINK.finditer(fenced_out(text)):
                raw = (match.group(1) or match.group(2)).strip('<>')
                if not raw or raw.startswith('#') or urlsplit(raw).scheme or raw.startswith('//'):
                    continue
                rawpath = unquote(raw.split('#', 1)[0].split('?', 1)[0])
                if not rawpath or '__' in rawpath or rawpath.startswith('{'):
                    continue
                candidate = (path.parent / rawpath).resolve()
                try:
                    candidate.relative_to(root)
                except ValueError:
                    add('block', 'link-outside-root', rel, 'A local link resolves outside the selected snapshot.')
                    continue
                if not candidate.exists():
                    add('block', 'broken-local-link', rel, 'A local Markdown link target does not exist.')
    meta = root / 'release' / 'metadata.json'
    if meta.is_file() and not meta.is_symlink():
        try:
            data = json.loads(meta.read_text(encoding='utf-8'))
            topics = data.get('topics', [])
            if not isinstance(topics, list) or any(not isinstance(t, str) for t in topics):
                add('block', 'topics', 'release/metadata.json', 'Topics must be a list of strings.')
            elif len(topics) > 20 or len(set(topics)) != len(topics) or any(not re.fullmatch(r'[a-z0-9-]{1,50}', t) for t in topics):
                add('block', 'topics', 'release/metadata.json', 'Topics exceed documented format/count or contain duplicates.')
        except (ValueError, OSError):
            add('block', 'metadata-json', 'release/metadata.json', 'Metadata is not readable valid JSON.')
    blocked = sum(f['level'] == 'block' for f in findings)
    reviews = sum(f['level'] == 'review' for f in findings)
    return {
        'schema_version': 1,
        'result': 'BLOCKED' if blocked else ('REVIEW' if reviews else 'CHECKS_PASSED'),
        'files_seen': len(files), 'text_files_checked': checked,
        'excluded_directories': skipped, 'blockers': blocked, 'review_items': reviews,
        'findings': findings,
        'limits': ['Selected current files only; Git history is not scanned.',
                   'No project commands, network requests, external-link checks or publishing performed.',
                   'Credential patterns are incomplete; no security, IP, growth or ranking guarantee.',
                   'Skill checks are lightweight sanity checks, not a complete YAML/spec validator.',
                   'Local Markdown links only; anchors and reference-style links are not validated.',
                   'Excluded directories and non-text content need separate publication review.']
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--json', action='store_true', help='Print machine-readable output to stdout.')
    args = parser.parse_args()
    try:
        report = audit(args.root)
    except (ValueError, OSError) as exc:
        print(f'Input error: {exc}', file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"{report['result']} | {report['files_seen']} files | {report['blockers']} blockers | {report['review_items']} review items")
        for item in report['findings']:
            print(f"[{item['level']}] {item['rule']}: {item['path']} — {item['message']}")
        print('This is a limited hygiene check, not authorization or proof of safety/virality.')
    return 1 if report['blockers'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
