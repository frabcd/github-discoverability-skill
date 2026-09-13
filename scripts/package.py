#!/usr/bin/env python3
"""Verify a reviewed file manifest, or bind only approved repository metadata.

No network or Git operations. Bind changes README identity and release metadata,
then regenerates hashes for exactly the existing allowlist. It never adds files.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath

IGNORE = {'.git', '.local', '__pycache__', '.venv', '.pytest_cache'}
MANIFEST = 'public-files.json'
TOKEN = '__REPO_FULL_NAME__'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def actual_files(root: Path) -> set[str]:
    result: set[str] = set()
    def visit(folder: Path) -> None:
        for entry in sorted(folder.iterdir()):
            rel = entry.relative_to(root).as_posix()
            if entry.name in IGNORE and entry.is_dir() and not entry.is_symlink():
                continue
            if entry.is_symlink():
                raise ValueError(f'Symlink not allowed in publication snapshot: {rel}')
            if entry.is_dir():
                visit(entry)
            elif entry.is_file() and rel != MANIFEST:
                result.add(rel)
    visit(root)
    return result


def manifest_paths(root: Path) -> tuple[dict, list[str]]:
    manifest_path = root / MANIFEST
    if manifest_path.is_symlink():
        raise ValueError('Manifest cannot be a symlink.')
    data = json.loads(manifest_path.read_text(encoding='utf-8'))
    if data.get('schema_version') != 1 or not isinstance(data.get('files'), list):
        raise ValueError('Unsupported manifest structure.')
    paths: list[str] = []
    for entry in data['files']:
        if not isinstance(entry, dict):
            raise ValueError('Malformed manifest entry.')
        raw = entry.get('path', '')
        if not isinstance(raw, str) or not raw or '\\' in raw or ':' in raw:
            raise ValueError('Invalid manifest path.')
        posix = PurePosixPath(raw)
        if posix.is_absolute() or '..' in posix.parts or posix.as_posix() != raw or raw == MANIFEST:
            raise ValueError('Unsafe or noncanonical manifest path.')
        if not re.fullmatch(r'[0-9a-f]{64}', str(entry.get('sha256', ''))):
            raise ValueError('Invalid digest.')
        paths.append(raw)
    if len(paths) != len(set(paths)):
        raise ValueError('Duplicate manifest path.')
    return data, paths


def verify(root: Path) -> dict:
    root = root.resolve()
    data, paths = manifest_paths(root)
    actual = actual_files(root)
    if actual != set(paths):
        raise ValueError(f'File set mismatch; missing={sorted(set(paths)-actual)}, extra={sorted(actual-set(paths))}')
    for entry in data['files']:
        if digest(root / entry['path']) != entry['sha256']:
            raise ValueError(f"Hash mismatch: {entry['path']}")
    return {'result': 'VERIFIED', 'allowlisted_files': len(paths),
            'note': 'Consistency check only; not a trusted signature or publication authorization.'}


def write_hashes(root: Path, paths: list[str]) -> None:
    data = {'schema_version': 1, 'files': [
        {'path': p, 'sha256': digest(root / p)} for p in sorted(paths)]}
    destination = root / MANIFEST
    destination.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')


def bind(root: Path, repository: str) -> dict:
    root = root.resolve()
    verify(root)
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})/[A-Za-z0-9][A-Za-z0-9_.-]{0,99}', repository):
        raise ValueError('Expected an approved GitHub OWNER/REPO, not a URL or command.')
    owner, name = repository.split('/', 1)
    if owner.endswith('-') or name.endswith('.git'):
        raise ValueError('Supply canonical OWNER/REPO, without trailing .git.')
    data, paths = manifest_paths(root)
    metadata_path = root / 'release/metadata.json'
    metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
    prior = metadata.get('repository')
    if prior not in {TOKEN, repository}:
        raise ValueError('Already bound to a different repository; do not silently rename.')
    if prior == repository:
        return verify(root)
    editable = ['README.md', 'README.zh-CN.md', 'release/metadata.json']
    if not set(editable).issubset(set(paths)):
        raise ValueError('Required publication metadata is not in the reviewed manifest.')
    updates = {}
    for rel in editable[:2]:
        updates[rel] = (root / rel).read_text(encoding='utf-8').replace(TOKEN, repository)
    metadata['repository'] = repository
    metadata['suggested_name'] = name
    updates[editable[2]] = json.dumps(metadata, indent=2)+'\n'
    for rel, text in updates.items():
        (root / rel).write_text(text, encoding='utf-8')
    write_hashes(root, paths)
    result = verify(root)
    result['bound_repository'] = repository
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('verify')
    binding = sub.add_parser('bind')
    binding.add_argument('repository')
    args = parser.parse_args()
    try:
        result = verify(args.root) if args.action == 'verify' else bind(args.root, args.repository)
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Package check failed: {exc}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
