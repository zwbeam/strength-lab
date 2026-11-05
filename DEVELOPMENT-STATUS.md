# Development status

Updated 2026-11-05. Branch: `development/reconciliation`.
Original main: `4cb58d8a4d30796246a83db752b8e420c8bc05c2`.
All existing commits through `374967f` preserved; source-scoped engine checkpoint:
`d387b81`; application/history checkpoint: `f5270fb`. No merge, force-push, deployment or release package.

## Training systems implemented

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
[research/programming-rules.json](research/programming-rules.json) contains eleven
verified quotation anchors and transcript hashes. The mechanical reconciliation
of 720 transcripts / 955,522 words remains intact; it is not a claim that all
lessons have been interpreted or that the app is medically validated.

## Verified

- 22 programming tests, 13 recovery tests, 3 completion tests, 3 backup tests;
  existing engine assertions and legacy smoke test also pass.
- Full snatch volume and density histories; multiple-week double-grind, heavy/light
  and club cycles; misses, incomplete work, technique correction/breakdown, pain,
  imbalance, duration changes, configurable gates and backup roundtrip.
- Actual HTTP app: 44 successful snatch exposures over about 19 simulated weeks,
  then load choice, failures, pain review and a missed month, saved/reloaded in
  actual browser storage. Phase citations are checked in the saved records.
- Separate real UI histories: six ABC workouts with light/heavy prescriptions,
  double-pair prerequisites and 20-minute carryover, custom club settings,
  active-draft guards and invalid equipment rejection.
- Six existing Chromium DOM suites and root/subpath offline browser tests pass.
- Baseline `374967f` to current service-worker upgrade preserves saved keys/draft
  byte-for-byte, reloads offline under mobile emulation and continues the old workout.
- Eleven provenance quote/hash checks, syntax and whitespace checks pass.

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
node --check app.js
node --check engine.js
node --check sw.js
python3 tests/research-provenance.py
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

1. Extend source-supported curricula and prerequisites to get-ups, single-arm club
   levels and additional movement-specific variants. Do not pretend the short
   two-hand club block reproduces a full multi-level program.
2. Validate richer program composition beyond configurable demand-category overlap;
   account for specific movements/implements rather than infer fatigue from a score.
3. Expand interpretation of the verified transcript collection; no source support
   should be inferred solely from keyword matches or title grouping.
4. Physical Android and installed-PWA checks. Chromium mobile emulation and worker
   upgrade checks pass but do not establish physical-device behavior.
5. Fresh cloud-task restoration. Runtime still reports the same onboarding instance
   and original source version; no tool is available to create a fresh task. It
   remains unverified, separately from browser reload and worker upgrade coverage.

No user setup/authorization is currently blocking development. These selected
training systems are implemented and tested; the full lifelong curriculum is
still a workbench, not a release.
