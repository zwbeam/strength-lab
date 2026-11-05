# Strength Lab V18 — Adaptive Training Beta

Upload the contents of this directory to the root of zwbeam/strength-lab, commit, then open https://zwbeam.github.io/strength-lab/?v=18. Before updating, export a full backup from Settings.

## Implemented
- Foundation five-session introduction and rolling five-session training cycles with no weekday lock.
- Per-movement history-based prescriptions: repeat, increase reps, increase load, reduce on repeated misses, and return-from-break adjustment.
- A simple rotating power/skill session after the first two training cycles. Advanced snatch and get-up skills require manual judgment; the app does not certify technique.
- Detailed movement logging: actual sets, reps per set, weight, rest, quality, notes; Performance Intelligence Report and expandable Training Log.
- Workout-specific warmups and cooldowns, collapsible technique guidance, existing timer.
- Local automatic draft saving and JSON/CSV export/import.

## Not implemented or guaranteed
- **Automatic GitHub cloud backup is not enabled.** A secure GitHub authorization service is needed. Export JSON externally until that exists.
- Only the previously linked direct videos are retained; the full video catalog is not yet independently verified.
- No full Android browser test has been run; this is a beta for feedback.
- Workouts use conservative programming heuristics, not medically validated readiness scores.

Data key remains strengthlab-data-v1. Clearing Chrome storage can delete training data.


V27: Workout for Life 10-minute warm-up and cooldown, baseline-first Foundation prescriptions, movement guides directly under headings, structured difficulty/technique/pain feedback, phase-aware training report, exercise details, dated notebook table, meaningful CSV export and unused asset cleanup.


## V31 preview — rolling full-body sessions

This version keeps the offline-first interface but uses a new `strengthlab-data-v31` local data key for a clean start.
Training starts immediately with three rolling workouts:

- A: double front squat, strict press, row
- B: two-hand swing, shield cast, suitcase carry
- C: single-arm clean, goblet squat, two-hand circles

The rotation advances only after saving a planned workout, regardless of calendar frequency.
Warmup, work and cooldown are now planned as 7 / 31 / 7 minutes (45 minutes total).
A main-work time estimate is displayed. **This is a planning target, not a hard timer
that automatically stops or changes prescriptions.** Take needed rest and modify
volume rather than rushing technique.

V30 browser data is not imported or erased: V31 uses its own storage key. Training history starts empty. Backup JSON remains format version 1.

Run `node v31-smoke-test.cjs` for basic sequence/migration checks.
