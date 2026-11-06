# Development status

Updated 2026-11-05. Branch: `development/reconciliation`.
Original main: `4cb58d8a4d30796246a83db752b8e420c8bc05c2`.
All existing commits through `374967f` preserved; source-scoped engine checkpoint:
`d387b81`; curriculum engine checkpoint: `9c70c0a`; curriculum application checkpoint: `2817a3f`.
The development branch is pushed to origin. No merge, force-push, deployment or release package.

## Persistent recovery verified

`development/reconciliation` is now stored on the existing GitHub repository,
not solely in this workspace. Separate fresh checkouts recovered `fe744c4` and
then `2817a3f`, passed Git object verification and the corresponding engine and
research tests. See [PERSISTENCE.md](PERSISTENCE.md). Main remained at the original
SHA. A fresh Codex task/cloud snapshot cannot be launched with available tools;
that distinct restoration check remains unverified.

## Training systems implemented

- Source-grounded get-up 3–10 **total-minute** progression with separate side rep
  counts, weak-side allowance, continuity and prerequisite checks.
- Single-arm club inside/outside/shield 4–20×5 continuous foundation volume,
  with between-movement rather than inter-set rest.
- Shared movement/skill/block definitions feed library, teaching links, prerequisites
  and generator. One-bout recovery reduces duration rather than leaving one set unchanged.
- Optional source-scoped snatch EMOM volume/density and double-kettlebell strength blocks.
- Explicit phase/load choices, owned-weight jump limits, matched pairs and skill gates.
- Heavy/light waves constrained by the last completed light exposure's work.
- Two-hand club timed profiles with editable bout length, set range and rest.
- Configurable exposure gates, #259-inspired stall alternatives, optional deloads,
  per-movement absence handling and explicit pain review/re-entry.
- Numeric side-difference logging, self-reported round cadence, and clear separation
  of performed work from progression evidence. Recovery adaptations do not claim
  exact numeric support from the source example.
- Program-specific deferred queues, whole-prescription duration fitting, overlap
  spacing, rolling-week training-day limits and heavy-movement caps.
- Actual Settings, workout and Progress integration; active-draft configuration guards.
- New profile/parameter choices preserve raw history; unchanged ABC defaults retain
  their original policy identity. Old V31/V32 data/interface remain available.

[TRAINING-RULES.md](TRAINING-RULES.md) explains source support versus app defaults.
[research/programming-rules.json](research/programming-rules.json) contains twenty-nine
verified quotation anchors and transcript hashes. The mechanical reconciliation
of 720 transcripts / 955,522 words remains intact; it is not a claim that all
lessons have been interpreted or that the app is medically validated.

[CURRICULUM-COVERAGE.md](CURRICULUM-COVERAGE.md) and the reproducible JSON inventory
screen all 720 full texts across 23 scoped systems: four implemented scopes,
twelve partial scopes and seven missing scopes. Candidate mentions are not
interpreted rules; implementation boundaries are explicit.

## Verified

- 22 programming tests, 10 curriculum tests, 13 recovery tests, 3 completion tests, 3 backup tests;
  existing engine assertions and legacy smoke test also pass.
- Full snatch volume and density histories; multiple-week double-grind, heavy/light
  and club cycles; misses, incomplete work, technique correction/breakdown, pain,
  imbalance, duration changes, configurable gates and backup roundtrip.
- New actual HTTP histories: 16 successful get-up exposures plus five adverse/
  recovery cases, and 34 successful three-movement club exposures plus one interrupted
  case (102 successful club movement records). Time units, side imbalance, pain,
  missed weeks, duration deferrals, rest structure, reload and earlier data were checked.
- Actual HTTP app: 44 successful snatch exposures over about 19 simulated weeks,
  then load choice, failures, pain review and a missed month, saved/reloaded in
  actual browser storage. Phase citations are checked in the saved records.
- Separate real UI histories: six ABC workouts with light/heavy prescriptions,
  double-pair prerequisites and 20-minute carryover, custom club settings,
  active-draft guards and invalid equipment rejection.
- Six existing Chromium DOM suites and root/subpath offline browser tests pass.
- Baseline `374967f` to current service-worker upgrade preserves saved keys/draft
  byte-for-byte, reloads offline under mobile emulation and continues the old workout.
- Sixteen provenance quote/hash checks, full-corpus matrix/registry checks, teaching-link/form checks, syntax and whitespace checks pass.

Browser simulations verify software behavior using self-reported workout input;
they do not establish physical training outcomes or technique competence.

## Reproduce

From `/workspace/strength-lab`:

```sh
node v31-smoke-test.cjs
node engine.test.cjs
node completion.test.cjs
node recovery.test.cjs
node backup.test.cjs
node programming.test.cjs
node curriculum.test.cjs
node --check app.js
node --check engine.js
node --check sw.js
python3 tests/research-provenance.py
python3 tests/curriculum-coverage.py
python3 tests/curriculum-library.py
python3 tests/curriculum-histories.py
python3 tests/browser-smoke.py
python3 tests/training-histories.py
python3 tests/programming-controls.py
python3 tests/service-worker-upgrade.py
```

Browser tests require Python Playwright and `/usr/bin/chromium`, present here.
Local socket/browser operations may require the supported execution approval flow.
The upgrade test uses a temporary copy of the committed baseline outside the repo.
Original-text verification: `python3 scripts/audit-transcripts.py /path/to/Transcripts`.
No dependency installation or application build is required.

Server: `python3 -m http.server 8000 --bind 127.0.0.1 --directory /workspace/strength-lab`.

## Highest-priority remaining work

1. Expand coherent foundational coverage where valuable: loaded hinge, complete
   ground transitions and traveling quadruped work. Hip drops and bear squats, get-up
   breakdowns, pendulum/pullover practice, unloaded hinge and push-up #609 are implemented.
2. Richer program composition than the current declared demand spacing; validate
   movement/implement-specific overlap without claiming to measure individual fatigue.
3. Other missing systems in the coverage matrix: competition jerk/long-cycle,
   ladders, mace, bodyweight ground/quadruped/push-pull, slam-ball and related resistance.
   Each requires source review and its own rules rather than borrowed snatch numbers.
4. Physical Android / installed-PWA checks. Keep static relative assets and pure
   browser engine compatible with eventual Capacitor packaging, but no APK or native
   packaging should begin before the core application is release-ready.
5. A genuinely fresh Codex task/snapshot test. Remote branch recovery is now proven;
   future-task authentication and environment restoration are separate, untested claims.

See NEXT-CONTINUATION.md for the exact next-task prompt. No user setup or
additional authorization is currently needed. Selected foundation systems are
implemented and tested; the complete curriculum remains unfinished.


## Interrupted-work recovery and persistence checkpoint — 2026-11-06

GitHub already contained `5bbae77` and `b07a0e7`, including the four get-up
breakdowns, five club intermediate drills, explicit skill/evidence gates,
unloaded hinge and push-up cycles. No committed work was lost. Backup changes
were uncommitted; `tests/backup-restore.py` did not exist and was recreated after
code review. Existing history was preserved.

V33 JSON backups now include active drafts, set logs, stage, notes and timer.
Drafts are validated before any storage changes. A write-ahead recovery journal
protects history/draft replacement and workout completion: caught failures roll
back; an interrupted transaction rolls back on reload. If rollback itself fails,
the previous snapshot remains readable and writes are blocked until recovery.
Failed workout saves retain the draft for retry; saved records identify their
source draft. Discard/reset/import use the same paired transaction. Existing
V33 backups without a draft remain supported; V31/V32 storage stays separate.

75 named Node tests pass, plus existing engine and legacy assertions. Actual
Chromium backup tests pass: malformed import rejection, paused timer/set restore,
second-write failure, failed-save retry without duplicates, interrupted-transaction
reload, failed startup recovery with blocked writes, and offline reload.
Browser fault injection tests software behavior, not hardware storage durability.


## Ground curriculum checkpoint — 2026-11-06

Added two-hand hip drops, single-hand hip drops and bear-squat practice to the
shared library/skills/engine/generator/settings. Recent clean two-hand evidence
and explicit skill review gate single-hand selection. App-default rep practice,
set ranges/rest and recovery gates are distinct from source teaching and timed
examples. Settings support dose changes without reusing incompatible evidence.

80 named Node tests now pass, plus engine/legacy assertions. Five new engine
cases cover generated multiweek histories, incomplete/imbalanced/poor-technique
work, recovery, missed weeks, equipment independence, pain and policy changes.
The real UI passed 15 generated ground sessions with explicit skill review,
shortened duration, missed-month re-entry/requalification, parent pain, offline
history and edited practice dose. The coverage matrix remains 23 scopes: four
implemented, twelve partial, seven missing. Twenty-nine source quotes/hashes verify.

Full release readiness, advanced specialty curricula, richer program composition,
physical Android/PWA testing and fresh Codex-task restoration remain unfinished.
No APK, release or main merge was produced.
