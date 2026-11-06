"""Screen every full transcript and document implementation coverage.
Candidate matches are discovery evidence, never automatically interpreted rules.
"""
from pathlib import Path
import json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
# status describes the scoped system in this row, not every lesson matching a term.
ROWS=[
 ('kb-hinge','Kettlebell deadlift / hinge / swing','partial',r'deadlift|\bhinge\b|\bswing\b',[704,288],['hingePractice','deadlift','swing'],'Unloaded-to-loaded two-hand deadlift practice has skill/evidence gates and app-default volume; swing defaults remain separate, and unilateral/stance pathways remain incomplete.'),
 ('kb-grinds','Kettlebell clean / press / squat','partial',r'clean|press|squat',[120,366,288],['clean','press','squat','doublePress','doubleSquat'],'Scoped double-grind examples and basic defaults; not every single-arm or stance variation.'),
 ('snatch-emom','Snatch EMOM volume / density example','implemented',r'snatch',[411,410],['snatch'],'Only the reviewed EMOM example; competition/complex variants are separate gaps.'),
 ('getup-base','Get-up alternating time-under-load goal','implemented',r'get.?up',[423,658,422,298,372,324],['getup'],'Prerequisite checklist and 3–10 minute alternating-single-rep goal; no automatic technique certification.'),
 ('getup-advanced','Get-up breakdown practice, advanced rep/complexity pathways','partial',r'get.?up|hip pass|hip drop',[422,298,372,324,658],['getupFloor','getupElbow','getupHand','getupHipPass'],'Four practice components have skill/evidence gates; advanced full-get-up same-side multi-rep cycles remain missing.'),
 ('kb-competition','Competition jerk / long cycle / marathon','missing',r'competition|long cycle|\bjerk\b|marathon',[287,464,465],[],'Do not apply hard-style snatch or double-grind numbers to these methods.'),
 ('kb-locomotion','Carries, walking and single-leg/stance work','partial',r'carry|walking|single leg|stagger|stance',[527,439,669],['carry'],'Suitcase carry only; walking, unilateral/stance variants and their own cycles remain missing.'),
 ('two-hand-club','Two-hand club levels and movement families','partial',r'two.hand|2.hand|heavy club',[3],['front','cast','circles'],'Isolated timed patterns exist; the complete seven-family multi-level curriculum does not.'),
 ('single-club-base','Single-arm club inside / outside / shield foundations','implemented',r'single.arm.*club|inside circle|outside circle|shield cast',[578,581,275,648,543],['clubInside','clubOutside','clubShield'],'Continuous 4–20×5 volume, balanced sides, and between-movement breaks; no automatic advanced-level assignment.'),
 ('single-club-next','Single-arm pendulums / pullovers / mills / swipes','partial',r'pendulum|pullover|\bmill\b|\bswipe\b',[578,260,265,269,624],['clubInsidePendulum','clubOutsidePendulum','clubFrontPullover','clubOutsidePullover','clubInsidePullover'],'Pendulum/pullover teaching with app-default volume and practice/skill gates exists; mills and swipes remain missing.'),
 ('rotational-footwork','Rotational footwork / pivots / staggered combinations','missing',r'pivot|footwork|stagger|rush step',[487,489,582],[],'No stance/pivot competency model or automatic complex combinations.'),
 ('mace','Mace 360, flows, leverage and complexity','missing',r'\bmace\b|\b360\b',[485,553,607],[],'Mace is not treated as an interchangeable club load; no mace generator.'),
 ('bodyweight-ground','Bodyweight get-ups / ground transitions','partial',r'body.?weight.*get.?up|hip drop|leg thread',[84,98,102],['hipDropTwoHand','hipDropSingleHand'],'Two-hand to single-hand hip-drop practice with skill/evidence gates; rocking leg-thread and complete get-up transitions remain missing.'),
 ('quadruped','Quadruped / crawling / bear patterns','partial',r'quadruped|crawl|bear squat',[87,100,554],['bearSquat'],'Bear-squat controlled mobility practice exists; traveling bear/cat crawls and flow transitions remain missing.'),
 ('push-pull-core','Push-up / pull-up / core progression','partial',r'push.?up|pull.?up|\bcore\b',[608,609,717],['pushup'],'Method #609 push-up EMOM wave is implemented; method #608, pull-ups and other core progressions remain missing.'),
 ('slam-ball','Slam-ball cycles and levels','missing',r'slam.?ball',[25,252,266],[],'No slam-ball equipment or prescription model.'),
 ('related-resistance','Sandbag / dumbbell / barbell integration','missing',r'sandbag|dumb.?bell|barbell',[482,514,703],[],'Discussed in the collection; no interchangeable-load assumptions or generator.'),
 ('climbing','Climbing / rope and sport-specific systems','missing',r'climbing|\brope\b|sport.specific',[121,555],[],'No sport-specific planning or climbing progression.'),
 ('mobility','Mobility / joint preparation / cooldown','partial',r'mobility|warm.?up|cool.?down|stretch',[550,670],[],'Pattern-matched preparation and duration budget only; full joint-specific lesson sequences remain missing.'),
 ('volume','Fixed-intensity volume programming','implemented',r'volume cycle|nerd math',[666,411,366,578],['snatch','doublePress','doubleSquat','clubInside'],'Implemented only within declared movement profiles, not a universal prescription.'),
 ('intensity','Density, heavy/light and intensity methods','partial',r'density|heavy.?light|light.?heavy|intensity',[410,228,403],['snatch','press'],'Snatch density and configurable waves exist; other apparatus-specific intensity methods require review.'),
 ('ladders','Ladders / reverse ladders / pyramids','missing',r'ladder|pyramid',[518,520],[],'No automatic ladder or work-equivalence planner.'),
 ('composition','Program composition / recovery / skill sequencing','partial',r'program design|tetris|recover|order of operation',[548,561,288,578],[],'Opt-in history-driven multi-block rotation, independent cycles, scoped unfinished queues, foundation support and recovery/time eligibility exist; complete Tetris and individualized fatigue models remain unfinished.'),
]
records=sorted([r for p in ROOT.glob('sources-*.json') for r in json.loads(p.read_text())],key=lambda r:r['id'])
assert len(records)==len({r['id'] for r in records})==720
registry=json.loads(subprocess.check_output(['node','-e',"const E=require('./engine.js');console.log(JSON.stringify({moves:E.MOVES,skills:E.SKILLS,blocks:E.BLOCKS}))"],cwd=ROOT))
rows=[]
for key,name,status,pattern,reviewed,moves,gap in ROWS:
    assert all(move in registry['moves'] for move in moves),(key,moves)
    regex=re.compile(pattern,re.I)
    titles=[r['id'] for r in records if regex.search(r['title'])]
    mentions=[]
    for source in records:
        match=regex.search(source['text'])
        if match:mentions.append({'id':source['id'],'excerpt':source['text'][max(0,match.start()-60):match.end()+120]})
    rows.append({'id':key,'system':name,'status':status,'screening_pattern':pattern,'candidate_title_ids':titles,'candidate_full_text_mentions':mentions,'source_reference_ids':reviewed,'implemented_movement_ids':moves,'boundary':gap})
inventory=[{'id':r['id'],'title':r['title'],'url':r['url'],'title_candidate_systems':[row['id'] for row in rows if r['id'] in row['candidate_title_ids']],'full_text_candidate_systems':[row['id'] for row in rows if any(m['id']==r['id'] for m in row['candidate_full_text_mentions'])]} for r in records]
report={'scope':'All 720 full texts screened. Keyword/title matches are candidate discovery, not manually validated rules or implementation proof. Status is manually scoped per row. Reference IDs are discovery links; close-read rule support is separately recorded in research/programming-rules.json and TRAINING-RULES.md.','systems':rows,'sources':inventory,'registry':registry}
(ROOT/'research/curriculum-coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# Curriculum coverage matrix','',report['scope'],'','All 720 records have an inventory entry, including those with no title matches. The JSON report includes full-text mention excerpts. Close reading and teaching validity are separate from this mechanical screening.','', '| System | Coverage | Discovery/reference IDs (zero-based) | Implemented / remaining boundary |','| --- | --- | --- | --- |']
for row in rows:lines.append('| '+row['system']+' | '+row['status']+' | '+', '.join('#'+str(i) for i in row['source_reference_ids'])+' | '+row['boundary']+' |')
lines+=['','The runtime library, prerequisite checklist and generator share `MOVES`, `SKILLS` and `BLOCKS` in `engine.js`. Tests validate those links. The matrix is not a claim that every matched title has been interpreted.','', 'Highest next priorities: richer program composition, reviewed remaining foundational bodyweight/ground systems, and release-readiness validation before advanced specialty variants. Mace, slam-ball, bodyweight and competition methods require their own models, not reused kettlebell numbers.','']
(ROOT/'CURRICULUM-COVERAGE.md').write_text('\n'.join(lines))
print('Inventoried',len(records),'full texts across',len(rows),'scoped systems')
