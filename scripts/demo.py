#!/usr/bin/env python3
"""Actually run preflight against synthetic before/after fixtures; no network."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('preflight_demo', ROOT/'skills/github-discoverability/scripts/preflight.py')
if spec is None or spec.loader is None:
    raise RuntimeError('Checker cannot be loaded.')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def run() -> dict:
    with TemporaryDirectory(prefix='discovery-demo-') as tmp:
        target = Path(tmp)
        (target/'README.md').write_text('# Example tool\n\n[Guide](missing.md)\n', encoding='utf-8')
        before = module.audit(target)
        (target/'README.md').write_text('# Example tool\n\nA synthetic documentation fixture.\n\n[Guide](guide.md)\n', encoding='utf-8')
        (target/'guide.md').write_text('# Guide\n\nThis is only a fixture, not an installable product.\n', encoding='utf-8')
        (target/'LICENSE').write_text((ROOT/'LICENSE').read_text(encoding='utf-8'), encoding='utf-8')
        after = module.audit(target)
    return {'fixture': 'synthetic', 'growth_evidence': False,
            'before': {'result': before['result'], 'rules': [f['rule'] for f in before['findings']]},
            'after': {'result': after['result'], 'blockers': after['blockers'], 'review_items': after['review_items']},
            'meaning': 'Only these local hygiene checks improved; no search/usage/stars claim.'}

if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
