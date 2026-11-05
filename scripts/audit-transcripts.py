"""Compare supplied originals against bundled text; no network or third party packages.
Usage: python3 scripts/audit-transcripts.py /path/to/Transcripts
"""
import hashlib
import json
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
originals = {}
for path in sorted(Path(sys.argv[1]).glob('*.txt')):
    text = path.read_text(encoding='utf-8-sig')
    match = re.search(r'VIDEO URL:\s*(\S+)', text)
    if not match or 'TRANSCRIPT:' not in text:
        raise ValueError(f'Missing metadata: {path.name}')
    url = match.group(1)
    if url in originals:
        raise ValueError(f'Duplicate original: {url}')
    originals[url] = (path.name, ' '.join(text.split('TRANSCRIPT:', 1)[1].split()))
index = json.loads((root/'source-index.json').read_text())
records = [item for path in sorted(root.glob('sources-*.json')) for item in json.loads(path.read_text())]
assert len({r['id'] for r in records}) == len(records), 'Duplicate source IDs'
assert {r['id'] for r in records} == {r['id'] for r in index}, 'Index/shard IDs differ'
by_id = {r['id']: r for r in index}
results = []
for record in records:
    filename, original = originals.get(record['url'], (None, ''))
    body = ' '.join(record['text'].split())
    entry = by_id[record['id']]
    results.append({'id': record['id'], 'url': record['url'], 'file': filename,
                    'text_matches': filename is not None and body == original,
                    'index_matches': entry['title'] == record['title'] and entry['words'] == len(body.split()),
                    'words': len(body.split()), 'sha256': hashlib.sha256(body.encode()).hexdigest()})
report = {'original_count': len(originals), 'indexed_count': len(index), 'shard_count': len(records),
          'total_words': sum(r['words'] for r in results),
          'missing_urls': sorted(set(originals) - {r['url'] for r in records}),
          'mismatches': [r for r in results if not r['text_matches'] or not r['index_matches']],
          'records': results,
          'scope': 'Whitespace-normalized text fidelity and metadata only; not interpretation or scientific validation.'}
(root/'research/transcript-audit.json').write_text(json.dumps(report, indent=2)+'\n')
print({key: value for key, value in report.items() if key not in ['records', 'mismatches']})
print('Mismatches:', len(report['mismatches']))
assert not report['missing_urls'] and not report['mismatches']
assert report['original_count'] == report['indexed_count'] == report['shard_count'] == 720
