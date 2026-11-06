# Exact next continuation prompt

**Current priority: finish publishing the isolated Android-friendly web preview.**
Read PREVIEW.md first. Do not add training features during this task. Source
checkpoint d5603e8 was verified; preview tooling reads committed runtime assets,
uses separate DEV identity/storage/lock/cache and has a real Android-sized local
coexistence test. Main and live deployment have not been changed.

Network settings are applied and GitHub/Pages access works. Existing Pages serves
main/root at https://zwbeam.github.io/strength-lab/; leave it unchanged. The separate
preview repository publication route is prepared in scripts/publish-preview.py.
GitHub returned integration HTTP 403 for repository creation. Required owner action:
create an empty public zwbeam/strength-lab-preview repository (no README/license/
gitignore). The chatgpt-codex-connector installation has all-repository selection.
Do not repeat the completed network-setting request.

Once the repo exists, run the guarded publisher, wait for Pages, then run
`python3 tests/preview-url.py --url https://zwbeam.github.io/strength-lab-preview/
--commit SOURCE_SHA` against the actual site. Do not claim the expected address is
live until it passes. Document verified source/deployment commits and update steps.
Preserve existing live file hashes, Pages settings and source main. The publisher
only writes the separate preview repository and normally pushes its preview branch.

The general development instructions below apply after that user objective is met.

Continue Strength Lab from the latest `origin/development/reconciliation`.
First verify that shell execution, GitHub and a representative browser test work;
environment status alone previously reported running while the executor was unusable.
Fetch origin, compare HEAD/status, preserve newer commits and inspect any uncommitted
work before applying it. Never reset or rewrite history.

Read DEVELOPMENT-STATUS.md, DEVELOPMENT-LOG.md, CURRICULUM-COVERAGE.md,
TRAINING-RULES.md and PERSISTENCE.md. Confirm ancestry of `b05b82c` (coordinated
programming), `ea80b41` (exclusive writer), `a68b180` (loaded hinge), `8e35d01`
(chronological selection), `1280712` (36-workout adverse histories) and `7e4a049`
(cadence feedback), or inspect newer work first. Later documentation commits may follow.

The interrupted local work was recovered and verified. The browser extension's
failure was a test assumption: a full advanced target does not fit a 15-minute
session. Preserve the corrected refusal/reduced-work checks. Do not reintroduce
that failing expectation or silently shrink targets for advancement credit.

Run relevant tests, especially `node composition.test.cjs`,
`node hinge-pathway.test.cjs`, `python3 tests/composition-feedback.py`,
`python3 tests/multi-tab.py`, `python3 tests/backup-restore.py` and source checks.
The repository has 98 named Node tests, engine/legacy checks and longer realistic
histories. Preserve the complete overview, free set logging, timers, adjustable
duration, offline library, saved data and all existing movement cycles.

Continue with high-impact composition/workload verification, accessibility and
release reliability; then source-reviewed complete ground/traveling quadruped or
intermediate club pathways. Read full relevant teaching sources before encoding
rules. Numeric programming, cadence, spacing and exposure app defaults must not
be attributed to transcripts without support. No automatic skill certification.

Use small independently tested commits and push each completed increment normally
to the existing development branch. Update status/log/coverage/rules and this prompt.
Do not merge main, force-push, publish a release or build an APK. Preserve relative
static assets and pure browser architecture for future Capacitor packaging.
If execution fails, stop dependent work, report the last successful pushed commit
and any uncommitted files, and give exact recovery steps without claiming tests ran.
