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
