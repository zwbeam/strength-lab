# Curriculum coverage matrix

All 720 full texts screened. Keyword/title matches are candidate discovery, not manually validated rules or implementation proof. Status is manually scoped per row. Reference IDs are discovery links; close-read rule support is separately recorded in research/programming-rules.json and TRAINING-RULES.md.

All 720 records have an inventory entry, including those with no title matches. The JSON report includes full-text mention excerpts. Close reading and teaching validity are separate from this mechanical screening.

| System | Coverage | Discovery/reference IDs (zero-based) | Implemented / remaining boundary |
| --- | --- | --- | --- |
| Kettlebell deadlift / hinge / swing | partial | #704, #288 | Unloaded hinge teaching and swing defaults exist; loaded deadlift and variant pathways remain incomplete. |
| Kettlebell clean / press / squat | partial | #120, #366, #288 | Scoped double-grind examples and basic defaults; not every single-arm or stance variation. |
| Snatch EMOM volume / density example | implemented | #411, #410 | Only the reviewed EMOM example; competition/complex variants are separate gaps. |
| Get-up alternating time-under-load goal | implemented | #423, #658, #422, #298, #372, #324 | Prerequisite checklist and 3–10 minute alternating-single-rep goal; no automatic technique certification. |
| Get-up breakdown practice, advanced rep/complexity pathways | partial | #422, #298, #372, #324, #658 | Four practice components have skill/evidence gates; advanced full-get-up same-side multi-rep cycles remain missing. |
| Competition jerk / long cycle / marathon | missing | #287, #464, #465 | Do not apply hard-style snatch or double-grind numbers to these methods. |
| Carries, walking and single-leg/stance work | partial | #527, #439, #669 | Suitcase carry only; walking, unilateral/stance variants and their own cycles remain missing. |
| Two-hand club levels and movement families | partial | #3 | Isolated timed patterns exist; the complete seven-family multi-level curriculum does not. |
| Single-arm club inside / outside / shield foundations | implemented | #578, #581, #275, #648, #543 | Continuous 4–20×5 volume, balanced sides, and between-movement breaks; no automatic advanced-level assignment. |
| Single-arm pendulums / pullovers / mills / swipes | partial | #578, #260, #265, #269, #624 | Pendulum/pullover teaching with app-default volume and practice/skill gates exists; mills and swipes remain missing. |
| Rotational footwork / pivots / staggered combinations | missing | #487, #489, #582 | No stance/pivot competency model or automatic complex combinations. |
| Mace 360, flows, leverage and complexity | missing | #485, #553, #607 | Mace is not treated as an interchangeable club load; no mace generator. |
| Bodyweight get-ups / ground transitions | partial | #84, #98, #102 | Two-hand to single-hand hip-drop practice with skill/evidence gates; rocking leg-thread and complete get-up transitions remain missing. |
| Quadruped / crawling / bear patterns | partial | #87, #100, #554 | Bear-squat controlled mobility practice exists; traveling bear/cat crawls and flow transitions remain missing. |
| Push-up / pull-up / core progression | partial | #608, #609, #717 | Method #609 push-up EMOM wave is implemented; method #608, pull-ups and other core progressions remain missing. |
| Slam-ball cycles and levels | missing | #25, #252, #266 | No slam-ball equipment or prescription model. |
| Sandbag / dumbbell / barbell integration | missing | #482, #514, #703 | Discussed in the collection; no interchangeable-load assumptions or generator. |
| Climbing / rope and sport-specific systems | missing | #121, #555 | No sport-specific planning or climbing progression. |
| Mobility / joint preparation / cooldown | partial | #550, #670 | Pattern-matched preparation and duration budget only; full joint-specific lesson sequences remain missing. |
| Fixed-intensity volume programming | implemented | #666, #411, #366, #578 | Implemented only within declared movement profiles, not a universal prescription. |
| Density, heavy/light and intensity methods | partial | #410, #228, #403 | Snatch density and configurable waves exist; other apparatus-specific intensity methods require review. |
| Ladders / reverse ladders / pyramids | missing | #518, #520 | No automatic ladder or work-equivalence planner. |
| Program composition / recovery / skill sequencing | partial | #548, #561, #288, #578 | Opt-in history-driven multi-block rotation, independent cycles, scoped unfinished queues, foundation support and recovery/time eligibility exist; complete Tetris and individualized fatigue models remain unfinished. |

The runtime library, prerequisite checklist and generator share `MOVES`, `SKILLS` and `BLOCKS` in `engine.js`. Tests validate those links. The matrix is not a claim that every matched title has been interpreted.

Highest next priorities: richer program composition, reviewed remaining foundational bodyweight/ground systems, and release-readiness validation before advanced specialty variants. Mace, slam-ball, bodyweight and competition methods require their own models, not reused kettlebell numbers.
