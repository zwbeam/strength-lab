# Training rules and provenance

This workbench implements selected programming lessons, not a finished synthesis
of all 720 transcripts or a technique/medical assessment. Exact quote anchors,
source URLs, hashes and interpretation boundaries are in
[research/programming-rules.json](research/programming-rules.json).

## Choose a program

In Settings, enter owned equipment and working weights first. A double-kettlebell
weight is **per bell**, and its matched pair must be confirmed separately. Under
Training programming choose a block, confirm only prerequisite skills you already
have, and save. Changing profiles or non-default parameters starts a separate
cycle without deleting history. Existing ABC defaults and their policy identity
are preserved when unchanged. Finish/discard an active draft before changing its
programming, equipment, next load or cycle.

| Profile | Transcript-supported scope | Strength Lab decisions |
| --- | --- | --- |
| Existing ABC volume | Fixed-intensity volume practice, #666 | Movement-specific preset sets/reps/rest, two clean exposures and ABC composition |
| Snatch EMOM | #411: 4–20 sets of 5 per side, one-minute rounds; one- or two-set increments | Explicit skill confirmation, exposure gate, equipment/load limits and recovery |
| Snatch density | #410: 16×6, 14×7, 12×8, 11×9, 10×10 per side, still one-minute rounds | Explicit choice only after volume endpoint; exposure gate; stop at endpoint |
| Double clean/press and front squat | #366: worked examples of 3–10 sets of 3, 4 or 5; three-minute rounds; #120 discusses paired fixed-weight programming | User chooses familiar load and rep scheme; matched-pair/skill gates and exposure threshold |
| Heavy/light wave | #228/#403: vary demand; heavier work stays below lighter work in total volume-load | Heavy reps, whole-set rounding, light-stage gate and coupled wave sequencing |
| Two-hand club timed practice | #3: timed practice, light before heavy and simple before complex | Isolated pattern bouts, set range, rest and promotion; not the full multi-level club program |

The density example applies only to snatches. Grinds, carries, rows and club
patterns never inherit those snatch numbers automatically. Complexity is never
advanced automatically. New advanced movements are not inserted into the existing
ABC rotation.

## What earns progression

A matching prescription must be completed at the planned load, with clean
technique, no pain, both sides/directions confirmed, and the configured number
of clean exposures (default two; adjustable 1–6). A correction or unsuccessful
exposure breaks the streak. Source examples additionally require the prescribed
intensity/volume rather than treating extra reps as equivalent evidence. Round
cadence confirmation is explicitly **self-reported**. A countdown is not proof
that a physical workout was performed correctly.

Separate numeric left/right actuals can record an imbalance; unequal performance
does not advance. Partial work, reduced readiness, rebuilds, re-entry and deloads
can be recorded but cannot promote a normal cycle. Clean reduced work can finish
an exposure without being endlessly carried forward as unfinished training.

Endpoints never raise load automatically. Only actual configured weights within
the app's jump limit are offered (default 25%, adjustable). Pair exercises use
confirmed pairs. If no suitable increment exists, maintain or deliberately review
equipment/settings. Increasing a permitted load restarts the volume cycle.
Heavy/light pairs are changed explicitly in Settings rather than silently altered.

## Stalls, recovery and longer-term scheduling

The optional #259-inspired stall alternative redistributes work into lower-rep
sets. Completed but poor technique uses approximately 80% reps; incomplete/too-hard
work uses approximately 60%. The classification and integer rounding are app
choices. Any extra set/rest cost must fit the session; the planner defers a whole
prescription rather than silently shortening it. Timed/cadence profiles use a
reduced-work rebuild, not this rep redistribution.

Pain holds persist across profile/weight changes. Explicit review resolves only
identified prior events; deleting earlier history cannot clear a later pain flag.
The return begins with reduced familiar work. #561 is a personal recovery account;
its percentages are not automatically prescribed as injury rehabilitation.

Settings exposes app defaults for absence threshold (14 days), re-entry fraction
(70%), low-readiness fraction (50%), optional deload frequency (disabled initially),
calendar spacing for overlapping demands (disabled initially), maximum training
days in a rolling week (six), and heavy/density movements per session (three).
These are app rules, not universal numbers from the transcripts. A deload interval
counts qualifying movement exposures, not calendar weeks. Shoulder, lower-body
and grip overlap categories are conservative approximations informed by #548;
they do not reproduce its complete club curriculum or evaluate individual fatigue.

Missed days never advance the rotation or create catch-up volume. Actual saved
work drives the queue. Deferrals are kept per block, so switching programs cannot
insert unrelated pending exercises. Complete prescriptions fit the selected
15–120-minute budget; warmup/cooldown remain included. If a full source cycle no
longer fits a short session, select more time or consciously choose reduced work
without advancement credit.

## Evidence and remaining scope

The actual HTTP application was tested with 44 successful snatch cycle exposures
across about 19 simulated weeks, followed by incomplete work, technique breakdown,
side imbalance, pain review and a missed month. A separate UI sequence saved six
ABC workouts showing light/heavy alternation, then exercised matched-pair/skill
gates, 20-minute movement carryover and custom timed club settings. Engine tests
cover complete double-grind, wave and club histories too.

This validates software transitions with self-reported data, not training efficacy.
Broader movement curricula beyond the selected get-up goal and single-arm club
foundations (including advanced levels and skills), automatic fatigue estimation and full source-by-source interpretation
remain unfinished. Physical Android/installed-PWA testing and a genuinely fresh
cloud-task restoration check remain distinct from browser emulation and worker
upgrade tests.

## Get-up and single-arm club curriculum continuation

The shared `MOVES` / `SKILLS` / `BLOCKS` registry now drives the library,
prerequisite checklist and workout generator. The library links the teaching
transcripts for each prerequisite, not only the final movement name.

| New system | Transcript support | App decisions and limits |
| --- | --- | --- |
| Alternating get-up time goal | #423: familiar complete single repetitions, 3–10 **total** minutes under load, optional 30-second steps; #658: repeat a goal with another weight | Self-confirmed floor press/roll/elbow/hand/hip-pass/overhead/full-movement checklist; two clean exposures; minimum elapsed-time acceptance and recovery fractions |
| Get-up side accounting | #423: start on the weaker side; an odd total may leave one extra repetition there | Actual complete reps are entered separately from elapsed seconds; the app accepts equal sides or one extra on the configured weaker side |
| Single-arm inside/outside/shield foundations | #578: continuous volume at fixed five reps per side, from a four-set example toward 20 sets; #581: rest between exercises, not within the volume sequence | Two clean exposures, estimated pace/transition allowance, prerequisite self-confirmation and conservative load offers |
| Prior two-hand club foundation | #275/#648/#543: single-arm technique builds on two-hand practice; #543 discusses at least three weights and a substantial training period | The app asks for explicit prior-foundation confirmation; it does not certify training years, technique, or readiness from a checkbox |

Get-up seconds are a total alternating time goal, never multiplied by two sides.
Logged left/right complete-repetition counts are not misread as seconds. The goal
can run in the integrated timer; elapsed time, continuity and safe controlled
technique remain self-reported. Incomplete time, absent side counts, unbalanced
strong-side extra reps or interrupted continuity cannot promote a cycle.

Single-arm club profiles never inherit snatch EMOM rest or density numbers.
Their per-set rest is zero. After a movement is finished, the app starts the
reviewed two-minute between-exercise example break. Planning includes those breaks
only between scheduled movements. Stop safely rather than forcing continuous
work when control is lost; interrupted work can be saved but earns no advancement.
A full three-movement endpoint fits the 45-minute app budget at the declared
estimate; slower performance may require more time. The estimate is not a speed
prescription or promise of physiological effect.

For one-bout get-up goals, low readiness, re-entry and deload reduce **duration**,
not an already-single set count. Those adapted numbers are labeled app defaults.
Neither get-up same-side multi-rep advanced sets (#658) nor club pendulums,
pullovers, mills, swipes or speed progressions are automatically unlocked.

[CURRICULUM-COVERAGE.md](CURRICULUM-COVERAGE.md) and its JSON inventory screen all
720 texts across 23 scoped systems. Mention matches are discovery candidates;
they do not turn missing programming methods into implemented or validated ones.

## Breakdown, intermediate and bodyweight pathways

Get-up practice now has four registry entries: floor press (#422), press/roll to
elbow (#298), hand support (#372), and hip-pass practice without the stand (#324).
The hand drill's light-load 3–10 rep route is discussed in #372. The other drills'
1×3–5 targets, all set counts/rest/pace, and the exposure gates are app defaults;
those teaching transcripts do not specify a universal numeric protocol.

The intermediate club block includes inside/outside pendulums (#260/#265), front
and outside pullovers (#269), and the controlled inside three-count pullover
(#624). #578 supports the family sequence and general volume method. This block's
2–6×3 starting protocol is an editable app choice, not falsely attributed as exact
numbers from those teaching lessons. It retains continuous practice within a
movement and between-movement rest, without importing snatch density or EMOM rules.
Mills, reverse mills and swipes are still not automatically selected.

New steps require both an explicit familiar-skill confirmation and recent clean
supporting practice at the current parent load/policy. The default is two supporting
exposures (configurable separately from a movement's own promotion gate). Incomplete,
corrected, recovery or stale practice cannot supply that evidence. The generator
includes needed supporting movements rather than leaving an empty intermediate
program. Continued clean intermediate practice can maintain previously established
supporting evidence, but cannot bypass a parent pain event, changed load, missing
skill review or an unpracticed ancestor. This is an app gate, not a source-specified
competency test. Skill checkboxes are never checked automatically from a log.

The unloaded hinge block uses the 2–3×10 **without load** teaching example in #704;
rest/pace/promotion are app choices. Zero external load is valid only on movements
explicitly marked bodyweight. It is not accepted as a valid working load for
kettlebell or club training. The existing weighted programs retain their behavior.

Push-up method #609 uses a conservative clean-rep baseline, a selected 40% or 50%
fraction, and a 10–30-round one-minute EMOM volume wave. The baseline input is
already conservative (exclude a failed/final rep); the app does not demand a new
maximum test. Whole-rep floor rounding, the clean-exposure gate and recovery rules
are app choices. A reviewed baseline/restart is explicit at the endpoint; it does
not erase prior history. A same-number baseline restart still begins a new cycle.
Short sessions defer a full EMOM prescription instead of granting credit for a
silently reduced target. Push-up method #608 and pull-up progression remain missing.

One-set breakdown recovery reduces reps. `performed` and progression eligibility
remain separate: even fully logged work with technique corrections cannot earn a
clean-exposure promotion. UI readiness, source links and generated prescriptions
all use the same movement/prerequisite registry and evidence functions.


## Backup and interrupted-work evidence

An active draft is not a completed training exposure. JSON backup/restore retains
its current stage, set confirmations, side counts, clock and prescription. Draft
validation occurs before replacing saved data. Completing a restored workout
uses the original prescription and the same completion/quality rules; incomplete
or failed work earns no additional credit. A failed save rolls history and draft
back together and can be retried. A recovery journal rolls back interrupted
paired writes before training decisions load. This is application data protection,
not a transcript-derived programming principle.


## Foundational bodyweight ground practice

The ground block shares the movement registry and evidence system with the other
programs. #84 teaches two-hand hip drops with quiet step-step transitions, stable
hand/foot placement and a stand before/after each set. #98 explicitly describes
the single-hand version as more advanced than the two-hand version. The app
requires explicit confirmation of both skills plus recent clean two-hand practice;
it never treats ground practice as loaded get-up certification. Parent pain,
changed policy, incomplete work or stale evidence prevents premature selection.

Hip-drop **rep practice** defaults to 2–4×3 per side, with 60-second rests. Those
numbers are Strength Lab choices, distinct from #84's 30-second timed example.
Start/end sets and reps are editable, and both-side confirmation/balanced reps
are required for progression. #100 teaches moving bear-squat mobility and offers
60/90-second examples. The app defaults to 2–4×60 seconds, allows a 30-second
regression, and labels the set range/rest/gates as app defaults. It does not
convert this into a traveling bear crawl or prescribe speed under fatigue.

Low readiness/re-entry/deload reduce sets with no progression credit. Equipment
is not required; zero external load is valid only for declared bodyweight
movements. Short sessions fit entire prescriptions and defer remaining work.
Advanced ground transitions, spinal rocking, leg-thread get-ups and crawling
remain separate source-review/implementation gaps. Quote/hash anchors for
#84/#98/#100 are included in the 30-entry provenance manifest.

Ground patterns share conservative lower-body/shoulder demand groups for optional
cross-block recovery spacing. Partial and low-readiness work still count as demand
without earning progression credit. All demand groups and day thresholds are app
defaults; #548 supports considering implement-specific demands, not this exact
mapping. Duplicate workout/draft identities or repeated movements within one
imported session are rejected instead of multiplying progression evidence.

## Coordinated long-term program (opt-in)

Settings can coordinate selected existing blocks across workouts. #548 discusses
separate kettlebell, two-hand and single-arm club days and their different demands;
#578 keeps single-arm volume/intensity/complexity choices distinct. The app does
not reproduce #548's unimplemented 70-movement club program, equate club and bell
loads, or insert its exercises as substitutes. Bodyweight/skill blocks may join
this app's rotation but are not falsely attributed to that source template.

The **Strength Lab selection rule** chooses the least recently practiced block
that is eligible and fits today, in selected order on ties. Only recorded actual
work counts as an attempt, including partial or reduced work. Each block retains
its own movement policies, cycles and unfinished queue. Partial work does not
promote a movement or repeatedly monopolize the schedule. Missed days create no
extra volume. Supporting foundation practice comes from the shared prerequisite
system. A whole prescription that does not fit is deferred, never silently reduced
for normal progression credit. A shorter eligible block can be selected instead.

Coordinated defaults are one calendar day between overlapping demands and two
between heavy/density workouts; both are editable 0–7 days. Stronger general
spacing still applies. A heavy/density attempt, including partial work, defers
other hard work until its interval passes. Ordinary volume/skill work may remain
eligible. Pain, weekly limits, prerequisites and equipment are mandatory gates.
These thresholds and the least-recent priority are original app choices, not
source-defined recovery calculations. No individualized fatigue score is claimed.

The compact "Why this workout?" panel explains emphasis, selection, supporting
practice and each selected block's eligibility. Volume/intensity/skill/recovery
labels describe the prescriptions, not measured physiological intensity.

A read-only or conflicted tab cannot log or save training evidence. Browser-managed
writer ownership and saved-value checks prevent updated tabs from overwriting one
another's drafts/history. A reader can export and inspect saved training; closing
the owner and reloading transfers editing with the current draft and timer.
This is data protection, not a training principle from a transcript.

## Unloaded-to-loaded hinge foundation

The optional kettlebell hinge foundation block adds a two-hand deadlift taught in
#704. It requires explicit hinge/deadlift familiarity plus recent clean unloaded
hinge practice. Missing/stale evidence schedules the unloaded parent; evidence
does not auto-confirm loaded technique. Child practice can maintain established
parent evidence under the same existing rules, but a new child load cannot bypass
stale parent evidence or pain. This block can join coordinated programming.

The loaded default is **2–4×5 with 90-second rests**; editable sets and 3/5/8 reps,
exposure gates, load increases and recovery adaptations are Strength Lab defaults.
#704's 2–3×10 example is explicitly **without weight**; it is not claimed as a
loaded prescription. Load selection remains explicit, owned and limited by the
configured jump cap. Short sessions fit whole prescriptions. Incomplete, corrected,
painful or reduced work never earns normal progression credit. Existing swing/ABC
cycles are preserved; deadlift completion does not auto-certify a swing or advanced
unilateral/stance hinge variation.


## Observed program cadence (Strength Lab planning feedback)

After at least four distinct training days within the past 56 days, the decision
panel estimates a return interval: mean spacing between those recorded days times
the number of selected blocks, rounded up to whole days. Empty sessions do not
count, and multiple workouts on one day count as one training day. Earlier/future
entries and backup array order cannot distort the observed chronological spacing.
Partial or reduced actual work counts as a training day, never as progression.

If that estimate exceeds the configurable absence window, the panel suggests
fewer active blocks. It does not shorten a prescription, certify a skill, increase
training frequency, add catch-up volume or override recovery. The sample threshold,
56-day window and formula are original app heuristics, not transcript-supported
numbers or physiological predictions. The panel also distinguishes clean-exposure
goals, reduced practice without credit, and completed cycles needing review.
