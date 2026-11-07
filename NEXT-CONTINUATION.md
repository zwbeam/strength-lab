# UX review 2 — Train notebook review checkpoint

Continue from the latest origin/development/reconciliation. Preserve all history.
Architecture checkpoint c482853 and integrated notebook c0a36de are ancestors.
Verified application source is 1e32b29363a247946ce4bb9c0b932b0a50bbc183,
deployed at 79c65b8165a2311a6ca6bf993b340b878486901b. Public HTTPS identity/80
assets and complete notebook acceptance passed. Later documentation commits may
follow; verify HEAD against GitHub first.
Read DEVELOPMENT-STATUS.md, DEVELOPMENT-LOG.md, TRAIN-NOTEBOOK-DESIGN.md,
PERSISTENCE.md, TRAINING-RULES.md and USER-EXPERIENCE-REVIEW.md.

The user authorized this Train/history rebuild after review 1. This milestone
must now follow build → test → isolated preview → user review → refinement.
Do not start another major redesign, redesign Learn or expand curriculum without
feedback. See PREVIEW.md for the exact publicly verified source/deployment/link.

Preserve ordered/provisional cycle inspection, full prescription and today's
normal-versus-adjusted plan, explicit preparation, compact prefilled log, optional
method-specific set editor, sticky wall-clock timer and instruction overlay.
Only final explicit affirmation records all non-skipped work; partial saves record
explicitly performed work only. A timer cannot grant work/skill credit. Get-up
side counts must be supplied. Zero-work stopped sessions do not skip a program day.

Historical corrections are reversible and append prior versions. Replay actuals,
rebuild unfinished queues and withdraw affected pending load choices. Preserve
all later actual workouts, explicit skills and recovery decisions. Older records
without original rx/load may be corrected, but changed legacy work cannot invent
new progression credit. Note-only changes preserve existing evidence. Explain
this limitation; never reconstruct an unknown original prescribed load as fact.

V33 storage keys, writer Web Lock, stale-write guard and paired journal remain.
New notebook drafts opt into variable actual sets; old drafts remain logged-only
and accepted. Import validates metadata/audit/actual credit before replacement.
See tests/notebook-review.py, tests/notebook-failures.py and
 tests/notebook-methods.py for real acceptance/fault/multiweek scenarios.
Run node test files individually (not only file-level test-runner wrappers), plus
relevant DOM, history, backup/multi-tab/upgrade and source-provenance checks.
Tests explicitly open optional editors/select Partial when testing old logged-only
flows; do not change actual programming rules to satisfy obsolete UI assertions.

Future preview publication uses scripts/publish-preview.py with a committed source
ref, separate zwbeam/strength-lab-preview repository/preview branch. Source pushes
alone do not publish Pages. Wait for build, run tests/preview-url.py with expected
source SHA and tests/notebook-review.py --url at the real HTTPS preview. TLS/proxy
remain configured. Keep production/main/Pages unchanged. No force push, release,
APK or production deployment. Keep relative static assets for eventual Capacitor.

Next: collect Android feedback on cycle clarity, adjustments, compact log,
completed-versus-partial affirmation, sticky timer/instruction return, actuals
editing and historical correction/replay. Refine feedback in small tested commits.
