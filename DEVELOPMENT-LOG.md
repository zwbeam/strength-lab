# Strength Lab development log

## 2026-11-05 — Source-scoped programming engine

Preserved branch history through `374967f`. Reviewed source lessons #3, #120,
#228, #288, #366, #403, #410, #411, #548 and #561, plus the previously reviewed
volume/warmup/stall material. Added `research/programming-rules.json` with eleven
verified quote anchors, URLs and normalized-text hashes. Source examples and
configurable app safeguards are separated explicitly.

Implemented optional snatch EMOM volume/density and double-kettlebell strength
blocks, club timed practice, heavy/light waves, explicit supported-cycle and
owned-load choices, prerequisite gates, stall alternatives, deload and recovery
scheduling. Complete prescriptions are fitted within the session duration;
missed days never generate catch-up volume. Existing ABC history remains on
its original policy identity. New profiles record their identity and provenance.

Fourteen programming-history tests pass, including full snatch cycles, multiple
weeks of double-grind and heavy/light work, failures, side differences, recovery,
missed weeks, durations, owned pairs and backup roundtrips. Existing engine,
completion, recovery, backup and legacy suites also pass. Eleven quote/hash
checks pass. Application wiring and final upgrade verification follow in a
separate focused commit.
