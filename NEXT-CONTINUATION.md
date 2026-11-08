# UX review 3 — recovery continuation (2026-11-08)

IMPORTANT: UX3 application code was already committed before the Codex remote turn failed. Do not restart UX3 implementation from scratch. GitHub comparison from e7a6a58 to development/reconciliation showed committed changes to app.js, engine.js, rolling-calendar.js, session-timer.js, programming-education.js, source rules, and new UX3 browser/failure tests. The prior UX2 continuation text below is historical, not the current work order.

Latest completed documentation checkpoint before this note: 5fee13b (UX3 user-approved requirements). Consult current branch HEAD; never assume this document's SHA remains latest.

DEVELOPMENT-LOG.md records UX3 calendar/UI integration and a successful Pixel 5 end-to-end acceptance, including activity replacement, pauses, timer, historical corrections, backup and offline. It explicitly leaves legacy UI regressions, remaining long histories and preview publication pending. Do not claim all tests passed or that the new preview is live. Existing public preview is the prior UX2 source 1e32b29 until a newer build is verified.

Immediate next steps:
1. Verify current branch HEAD and review changes since e7a6a58, including tests and code for the new rolling-calendar and pause/activity behavior.
2. Run remaining legacy DOM/browser tests, long histories, source/provenance and storage regressions. Fix genuine failures; update obsolete UI selectors/fixtures only when old controls were intentionally removed.
3. Test timer, date shifts, beginner spacing, manual moves, activity editing, pause/resume and partial-work integrity under reload/offline/multi-tab conditions.
4. Finish integration checks, update documentation and run isolated preview publisher for the exact tested source commit. Verify actual public HTTPS build, assets and identity. Never modify main/production or create APK.
5. Request physical Android review. Only then plan next UX adjustments.
6. Continue transcript integration from research/review-checkpoint.json and RESEARCH-INTEGRATION-AUDIT.md. 720 is the reconciled inventory, NOT 720 fully manually reviewed. The historical 504/720 total is unverified by the available ledger; retain uncertainty. New anchored close-read batch #404, #606, #515, #527 has been integrated in specific limited ways. Do not overwrite source provenance or manufacture further review counts.

Preserve V33 local data, journal, Web Lock, reversible history corrections, prescription-vs-actual separation and incomplete-work carry-forward. No force pushes, production changes, merge, release or APK.

---

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
