"""Check corpus coverage and links without treating screening as interpretation."""
from pathlib import Path
import json,subprocess
root=Path(__file__).resolve().parents[1]
report=json.loads((root/'research/curriculum-coverage.json').read_text())
records={r['id']:r for p in root.glob('sources-*.json') for r in json.loads(p.read_text())}
assert {r['id'] for r in report['sources']}==set(records) and len(report['sources'])==720
registry=json.loads(subprocess.check_output(['node','-e',"const E=require('./engine.js');console.log(JSON.stringify({moves:E.MOVES,skills:E.SKILLS,blocks:E.BLOCKS}))"],cwd=root))
assert report['registry']==registry,'Regenerate coverage after changing the shared registry'
for row in report['systems']:
 assert row['status'] in ['implemented','partial','missing']
 assert row['boundary']
 assert all(id in records for id in row['source_reference_ids'])
 assert all(id in registry['moves'] for id in row['implemented_movement_ids'])
 for mention in row['candidate_full_text_mentions']:assert mention['excerpt'] in records[mention['id']]['text']
print(f"PASS: 720 source inventory entries, {len(report['systems'])} scoped systems, mention evidence and shared runtime definitions")
