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
