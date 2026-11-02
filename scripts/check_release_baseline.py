"""Ensure the bilingual RPC catalogs cover the pinned release audit manifest."""
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'docs/contributing/v0.9.2-audit.json').read_text())
expected = set(manifest['registered_paths']) | set(manifest['greylist_conditional_paths'])
for suffix in ['', '.en']:
    page = root / f'docs/03_Operators/funod-rpc{suffix}.md'
    text = page.read_text()
    actual = set(re.findall(r'/v1/[a-z_]+/[a-z_0-9]+', text))
    missing, extra = expected - actual, actual - expected
    if missing or extra:
        raise SystemExit(f'{page.name}: missing={sorted(missing)}, extra={sorted(extra)}')
    if 'target_version: v0.9.2' not in text or manifest['source_revision'] not in text:
        raise SystemExit(f'{page.name}: missing pinned release provenance')
    for method in ['get_optimization_suggestions', 'get_cache_analysis', 'get_maintenance_needs']:
        if f'| `{method}` |' not in text:
            raise SystemExit(f'{page.name}: missing method table row: {method}')
assert len(manifest['registered_paths']) == 86
assert len(manifest['greylist_conditional_paths']) == 3
print('PASS: both RPC catalogs cover all 86 v0.9.2 paths and 3 conditional greylist paths')
