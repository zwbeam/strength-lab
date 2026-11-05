"""Validate that implemented rule citations still refer to the verified corpus."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
records={r['id']:r for p in root.glob('sources-*.json') for r in json.loads(p.read_text())}
audit={r['id']:r for r in json.loads((root/'research/transcript-audit.json').read_text())['records']}
rules=json.loads((root/'research/programming-rules.json').read_text())['rules']
for rule in rules:
    source=records[rule['source_id']]
    text=' '.join(source['text'].split())
    digest=hashlib.sha256(text.encode()).hexdigest()
    assert digest==rule['normalized_text_sha256']==audit[source['id']]['sha256']
    assert rule['quote'] in text
    assert rule['url']==source['url']
    assert rule['app_defaults_not_claimed_as_source_rules']
print(f'PASS: {len(rules)} rule quotations and hashes match the previously verified transcript corpus')
