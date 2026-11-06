"""Verify instruction evidence and exact video mappings against the existing corpus."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
review=json.loads((ROOT/'research/movement-instruction.json').read_text())
generated=json.loads(subprocess.check_output(['node','-e',"console.log(JSON.stringify(require('./movement-instruction.js')))"],cwd=ROOT))
records={r['id']:r for f in ROOT.glob('sources-*.json') for r in json.loads(f.read_text())}
audit={r['id']:r for r in json.loads((ROOT/'research/transcript-audit.json').read_text())['records']}
assert review['entries']==generated['entries'] and review['links']==generated['links']
for id,source in generated['sources'].items():
 record=records[int(id)];digest=hashlib.sha256(' '.join(record['text'].split()).encode()).hexdigest()
 assert source['sha256']==digest==audit[int(id)]['sha256']
 assert source['url']==record['url'] and source['title']==record['title'] and source['timestamps'] is None
quotes=0
for entry in review['entries'].values():
 for evidence in entry['evidence']:
  assert evidence['quote'] in ' '.join(records[evidence['sourceId']]['text'].split());quotes+=1
 for video in entry['videoSourceIds']:assert str(video) in generated['sources']
mapped=sum(bool(e['videoSourceIds']) for e in review['entries'].values())
print(f'PASS: {len(review["entries"])} canonical outlines, {quotes} exact evidence quotes, {len(generated["sources"])} source hashes, {mapped} mapped movement videos; no invented timestamps')
