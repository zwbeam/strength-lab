# UX review 1: user-review checkpoint

Continue from the latest origin/development/reconciliation. Preserve all history.
Timer milestone: 2d97220. Learn milestone: 7c6f2c0. The separate preview build
uses source 7c6f2c0070840db3da4a1c813ae57e1bb8411e92; see PREVIEW.md for verification.

Read USER-EXPERIENCE-REVIEW.md and the latest DEVELOPMENT-LOG.md before acting.
The user requires build → test → preview → user review → refinement. Do not begin
another major interface redesign before user feedback. Implement feedback in
small verified increments; do not mistake automated tests for UX approval.

Manual is the new-session default; existing drafts and preference snapshots remain
compatible. Timer-only events cannot log sets or grant progression. Exercises and
Pathways share the registry, actual eligibility and history. Learned is explicit
self-reported familiarity, never mastery or a prerequisite bypass. All 31 lessons
remain readable; 29 have corpus metadata video mappings, carry/front squat have
explicit gaps. Some videos cover programming rather than full technique. No
verified timestamps or physical Android playback claim exists.

First inspect Git status, compare/fetch remote and preserve newer commits. GitHub
credentials briefly returned 401 during this task but later recovered; never ask
for raw tokens. Use the existing gh credential helper per command if required.
Run node test files individually plus tests/timer-review.py, tests/learn-review.py,
tests/learning-provenance.py, tests/backup-restore.py, tests/multi-tab.py and relevant
history/upgrade regressions when changes warrant them.

Normal development pushes do not deploy Pages. After verified application changes,
use scripts/publish-preview.py for the separate preview repository; wait for Pages
and run tests/preview-url.py with the expected source commit and actual HTTPS URL.
Preserve the original app/main/Pages, saved history, full overview, free set logging,
relative assets and offline research. No main merge, force push, release or APK.

Next task: collect Android feedback on timer interaction/mode clarity, finding
lessons, focused maps and external video opening. Refine only after that review.
