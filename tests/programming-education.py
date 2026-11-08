"""Runtime programming education mappings and explicit integration checkpoint."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
text=(ROOT/'programming-education.js').read_text();data=json.loads(text.split('window.ProgrammingEducation=',1)[1].rstrip().removesuffix(';'))
records={r['id']:r for f in ROOT.glob('sources-*.json') for r in json.loads(f.read_text())}
for id,source in data['sources'].items():
 r=records[int(id)];assert source['url']==r['url'] and source['title']==r['title'];assert source['sha256']==hashlib.sha256(' '.join(r['text'].split()).encode()).hexdigest()
for topic in data['topics']:
 assert topic['principle'] and topic['app'] and topic['limits']
 assert all(str(i) in data['sources'] for i in topic['sourceIds'])
checkpoint=json.loads((ROOT/'research/review-checkpoint.json').read_text());assert checkpoint['full_manual_review_total'] is None and len(checkpoint['new_close_read_integrated_batch'])==4
assert {x['id'] for x in checkpoint['new_close_read_integrated_batch']}=={404,606,515,527}
print(f'PASS: {len(data["topics"])} runtime Programming lessons, exact corpus metadata/hashes, explicit principle/app/limits and four-source integrated checkpoint; no invented full-review count')
