# Exact next continuation prompt

**Current priority: finish publishing the isolated Android-friendly web preview.**
Read PREVIEW.md first. Do not add training features during this task. Source
checkpoint d5603e8 was verified; preview tooling reads committed runtime assets,
uses separate DEV identity/storage/lock/cache and has a real Android-sized local
coexistence test. Main and live deployment have not been changed.

The environment blocked api.github.com and zwbeam.github.io. A draft allowing
those two domains was saved but requires the user to review/save and Publish the
environment. Verify actual network readiness after that, then inspect GitHub Pages
settings/permissions and choose an additive preview publication route preserving
the live app and its update mechanism. Do not infer that pushing development
publishes Pages. Run tests/preview-url.py against the actual HTTPS URL and expected
SHA before reporting a live link. Document the confirmed publication/update route.

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
