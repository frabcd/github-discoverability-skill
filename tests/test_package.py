from __future__ import annotations
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

PREFLIGHT = load('preflight_tests', ROOT/'skills/github-discoverability/scripts/preflight.py')
PACKAGE = load('package_tests', ROOT/'scripts/package.py')

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.write('README.md', '# Demo\nA fixture.\n')
        self.write('LICENSE', 'A fixture license; not a legal evaluation.\n')
    def tearDown(self):
        self.tmp.cleanup()
    def write(self, path, text):
        dest=self.root/path; dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding='utf-8')
    def report(self): return PREFLIGHT.audit(self.root)
    def rules(self): return {f['rule'] for f in self.report()['findings']}
    def test_clean_fixture(self): self.assertEqual(self.report()['result'], 'CHECKS_PASSED')
    def test_missing_license(self):
        (self.root/'LICENSE').unlink(); self.assertIn('license', self.rules())
    def test_missing_readme(self):
        (self.root/'README.md').unlink(); self.assertIn('readme', self.rules())
    def test_broken_link(self):
        self.write('README.md', '# Demo\n[guide](absent.md)'); self.assertIn('broken-local-link', self.rules())
    def test_existing_local_link(self):
        self.write('guide.md', '# Good'); self.write('README.md', '[guide](guide.md)')
        self.assertEqual(self.report()['blockers'], 0)
    def test_outside_link(self):
        self.write('README.md', '[outside](../private.md)'); self.assertIn('link-outside-root', self.rules())
    def test_code_fence_not_link_checked(self):
        self.write('README.md', '# Demo\n```md\n[x](absent.md)\n```\n')
        self.assertNotIn('broken-local-link', self.rules())
    def test_sensitive_filename(self):
        self.write('.env.local', 'EXAMPLE=true'); self.assertIn('sensitive-name', self.rules())
    def test_template_env_allowed(self):
        self.write('.env.example', 'EXAMPLE=replace-me'); self.assertNotIn('sensitive-name', self.rules())
    def test_credential_is_redacted(self):
        fake = 'gh' + 'p_' + 'A'*36
        self.write('config.txt', fake)
        report=self.report(); self.assertIn('credential-shape', {x['rule'] for x in report['findings']})
        self.assertNotIn(fake, json.dumps(report)); self.assertNotIn(str(self.root), json.dumps(report))
    def test_private_key_marker(self):
        self.write('config.txt', '-----BEGIN '+'PRIVATE KEY-----\nnot-a-real-key')
        self.assertIn('credential-shape', self.rules())
    def test_bad_skill_name(self):
        self.write('skills/demo/SKILL.md', '---\nname: other\ndescription: Example.\n---\n# Demo')
        self.assertIn('skill-name', self.rules())
    def test_good_skill_name(self):
        self.write('skills/demo/SKILL.md', '---\nname: demo\ndescription: Example.\n---\n# Demo')
        self.assertNotIn('skill-name', self.rules())
    def test_topic_limit(self):
        self.write('release/metadata.json', json.dumps({'topics':[f'topic-{i}' for i in range(21)]}))
        self.assertIn('topics', self.rules())
    def test_repo_binding_is_review(self):
        self.write('README.md', '# Demo\n__REPO_FULL_NAME__')
        self.assertEqual(self.report()['result'], 'REVIEW')
    def test_symlink_not_followed(self):
        try: (self.root/'escape').symlink_to(self.root.parent, target_is_directory=True)
        except OSError: self.skipTest('Symlink privilege unavailable')
        self.assertIn('symlink', self.rules())
    def test_large_file_reported(self):
        self.write('large.txt', 'x'*(PREFLIGHT.MAX_BYTES+1)); self.assertIn('large-file', self.rules())
    def test_audit_does_not_write(self):
        before={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.report()
        after={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before,after)
    def test_cli_missing_target_fails(self):
        proc=subprocess.run([sys.executable, str(ROOT/'skills/github-discoverability/scripts/preflight.py'), str(self.root/'missing')], capture_output=True, text=True)
        self.assertEqual(proc.returncode,2)

class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        (self.root/'release').mkdir()
        for name in ['README.md','README.zh-CN.md']:
            (self.root/name).write_text('__REPO_FULL_NAME__', encoding='utf-8')
        (self.root/'release/metadata.json').write_text(json.dumps({'repository':'__REPO_FULL_NAME__'}),encoding='utf-8')
        PACKAGE.write_hashes(self.root, sorted(PACKAGE.actual_files(self.root)))
    def tearDown(self): self.tmp.cleanup()
    def test_verify(self): self.assertEqual(PACKAGE.verify(self.root)['result'],'VERIFIED')
    def test_corruption_blocked(self):
        (self.root/'README.md').write_text('changed',encoding='utf-8')
        with self.assertRaises(ValueError): PACKAGE.verify(self.root)
    def test_extra_file_blocked(self):
        (self.root/'private.txt').write_text('private',encoding='utf-8')
        with self.assertRaises(ValueError): PACKAGE.verify(self.root)
    def test_binding(self):
        PACKAGE.bind(self.root,'example-owner/example-repo')
        self.assertEqual((self.root/'README.md').read_text(), 'example-owner/example-repo')
        self.assertEqual(PACKAGE.verify(self.root)['result'],'VERIFIED')
    def test_binding_idempotent(self):
        PACKAGE.bind(self.root,'example-owner/example-repo')
        before=(self.root/'public-files.json').read_bytes()
        PACKAGE.bind(self.root,'example-owner/example-repo')
        self.assertEqual(before,(self.root/'public-files.json').read_bytes())
    def test_different_rebind_blocked(self):
        PACKAGE.bind(self.root,'example-owner/example-repo')
        with self.assertRaises(ValueError): PACKAGE.bind(self.root,'other-owner/other-repo')
    def test_invalid_destination_blocked(self):
        with self.assertRaises(ValueError): PACKAGE.bind(self.root,'owner/repo;bad-command')
    def test_unsafe_manifest_path_blocked(self):
        (self.root/'public-files.json').write_text(json.dumps({'schema_version':1,'files':[{'path':'../escape','sha256':'0'*64}]}))
        with self.assertRaises(ValueError): PACKAGE.verify(self.root)

if __name__ == '__main__': unittest.main()
