# Development status

Work continues on `development/reconciliation`. Preserve existing history and
raw training data. No merge into main, force-push, release or APK is authorized.

## Interrupted work recovered

Remote `b07a0e7` already contained `5bbae77` and `b07a0e7`: four get-up breakdowns,
five single-arm club intermediate drills, explicit skill/recent-practice gates,
unloaded hinge, push-up #609 and multiweek tests. Nothing committed was lost.
Backup edits survived uncommitted; the proposed `tests/backup-restore.py` was
absent. Those edits were reviewed, completed, tested and pushed at `6c3df46`.
Expanded failure tests are at `c266c97`; ground foundations are at `da8af31`.
Later normally pushed checkpoints are recorded in Git history and the log.

## Implemented application

- Shared movements, skills, profiles and blocks power the library, Settings,
  prerequisites, workout generator, history and progression.
- Existing ABC, snatch EMOM volume/density, double-kettlebell grinds, heavy/light
  waves, two-hand club practice and matched-pair/load constraints remain intact.
- Get-up alternating total-time goals plus floor press → elbow → hand → hip pass
  practice; single-arm inside/outside/shield volume plus pendulums/pullovers.
- Unloaded hinge and explicit baseline/restart push-up EMOM volume.
- Ground block: two-hand → single-hand hip drops and bear-squat mobility.
  Source teaching/timed examples are distinct from editable app practice doses.
- Explicit self-confirmed skill review and recent clean parent evidence are both
  required. Parent pain, load/policy changes, incomplete work and stale prerequisites
  cannot be bypassed by prior descendant practice. Supporting practice is generated.
- Movement-specific progression, absence/re-entry, low readiness, technique/pain
  review, optional deloads, whole-prescription duration fitting and deferred queues.
  Performed work and progression evidence are separate; incomplete work never promotes.
- Recovery spacing includes ground work and applies across blocks, including partial
  and recovery exposures. Missing prerequisites, pain, scheduling and equipment each
  explain why training is unavailable; more time does not clear those holds.
- Full overview, free set logging, integrated/rest timers, adjustable duration,
  offline research library and saved history remain available. V31/V32 remain separate.

## Backup and persistence

V33 JSON exports include the active draft, stage, set logs, confirmations, notes
and clock. Old V33 backups without a draft remain supported. Validation precedes
storage changes, including duplicate session/draft/movement rejection.

History/draft changes use a write-ahead rollback journal. Caught save failures
restore old keys; interrupted transactions recover before loading training data.
If rollback fails, the old snapshot remains readable and saved writes are blocked
until recovery succeeds. Workout-save failure retains the draft for safe retry.
Import/reset/discard use the same paired transaction. These browser API guarantees
do not establish physical storage durability or concurrent multi-tab isolation.

## Verified in this resumed task

- 82 named Node tests, plus engine assertions and legacy smoke checks.
- Real Chromium backup tests: paused/running clocks and completed sets restored;
  malformed/duplicate imports rejected unchanged; journal-write, second-key and
  discard/save removal failures; safe retry; interrupted commit and failed startup
  rollback with blocked writes; later recovery; offline reload.
- Actual generated histories: 42-exposure push-up wave; get-up breakdown and club
  intermediate pathways; 15 new ground sessions, skill confirmation, short sessions,
  equipment independence, stale-prerequisite requalification, pain and edited doses.
- Existing histories: 44 snatch workouts over 19 simulated weeks; get-up 3–10-minute
  progression; 34 successful three-movement club workouts; six ABC heavy/light
  workouts, equipment/pair gates and duration carryover.
- Six timer/focus/duration/library DOM suites; actual library/teaching links;
  root/subpath offline workflows; baseline-to-current worker upgrade preserving
  saved keys/draft byte-for-byte and continuing an old workout offline.
- 29 quotation/hash anchors and all-720-source coverage/registry checks; syntax
  and whitespace checks. Fault injection and self-reported workouts test software
  behavior, not physical training outcomes or medical/technique competence.

The 23-system curriculum matrix has four implemented scopes, twelve partial and
seven missing. All 720 texts were mechanically inventoried; that does not mean
all teaching has been interpreted. See CURRICULUM-COVERAGE.md and TRAINING-RULES.md.

## Highest-impact remaining work

1. Richer composition across programs and apparatus: current demand groups are
   conservative app defaults, not an individualized fatigue model or complete Tetris.
2. Reviewed foundational gaps: loaded hinge/deadlift, complete ground transitions,
   traveling quadruped practice; then remaining intermediate club systems. Do not
   add low-value variations simply to increase the movement count.
3. Backup/import and concurrent-tab stress testing, broader accessibility and
   release-readiness checks. Current storage transactions are single-tab recovery.
4. Physical Android/installed-PWA verification. Keep relative static assets and pure
   browser engine compatible with future Capacitor, but do not package an APK yet.
5. Fresh Codex-task/environment restoration. Separate GitHub checkouts can be tested;
   available tools cannot launch a genuinely fresh Codex task or verify its login.

## Reproduce

Run all root `*.test.cjs` with Node, plus `node v31-smoke-test.cjs`.
Run relevant `tests/*.py` with Python; browser suites require Playwright and
`/usr/bin/chromium` (available here) and permitted local browser/socket access.
Key suites: `tests/backup-restore.py`, `tests/ground-histories.py`,
`tests/bodyweight-histories.py`, `tests/pathway-histories.py`,
`tests/training-histories.py`, `tests/curriculum-histories.py`,
`tests/programming-controls.py`, `tests/browser-smoke.py`,
`tests/service-worker-upgrade.py`, `tests/research-provenance.py`,
`tests/curriculum-coverage.py`, `tests/curriculum-library.py`.
No dependency installation or build is required in this environment.

Read DEVELOPMENT-LOG.md and NEXT-CONTINUATION.md before the next changes.

Independent GitHub recovery was repeated at `d99a153`: fresh clone/object checks,
all Node suites, provenance/coverage, and actual backup/ground browser tests pass.
See PERSISTENCE.md. Fresh Codex-task restoration is still unavailable to test.
