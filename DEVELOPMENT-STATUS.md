# Development status

Continue on `development/reconciliation`; preserve commits, research and raw
training data. No main merge, force-push, release or APK is authorized.

## UX review 1 milestone (2026-11-06)

Timer repair checkpoint: `2d97220`. Learn now provides registry-backed Exercises,
focused Pathways, practical instruction, eligibility/history statuses and exact
video metadata links. All 31 movements are represented; 29 have video mappings,
carry/front squat remain explicit gaps. Existing training cycles are preserved.
Manual timer mode is the new-session default; Automatic/Hybrid are available.
See USER-EXPERIENCE-REVIEW.md before further major interface work. Automated tests
are evidence of behavior, not user approval. Pause for Android user review after
publication; programming coverage and physical-device testing remain incomplete.

## Current recovery checkpoint

The executor was restored on 2026-11-06. Shell, GitHub, Node and real Chromium
operations now work. GitHub contained all reported checkpoints with no newer work:
`b05b82c` coordinated programming, `ea80b41` multi-tab protection and `a68b180`
loaded hinge practice. Main remains `4cb58d8`.

Three uncommitted files survived. Their changes were reviewed rather than blindly
recreated. Chronological selection was tested/pushed at `8e35d01`. The unfinished
browser extension had incorrect time-budget assumptions; the corrected 36-workout
workflow was tested/pushed at `1280712`. Cadence feedback is at `7e4a049`.
Later documentation commits may follow. The log and Git history are authoritative.

## Implemented training application

- Existing ABC, snatch EMOM volume/density, double-kettlebell strength, heavy/light
  waves, two-hand club and single-arm continuous volume retain independent cycles.
- Shared movement/skill/profile/block registries drive the library, Settings,
  teaching links, prerequisites, workout generation, history and progression.
- Get-up floor → elbow → hand → hip-pass practice; club pendulums/pullovers;
  unloaded hinge → loaded two-hand deadlift; push-up EMOM; two-hand → single-hand
  hip drops and bear-squat practice. Source teaching and numeric app defaults
  remain explicitly distinct. No automatic technique certification is claimed.
- Recent clean parent evidence and explicit skill confirmation gate new pathways.
  Pain, changed load/policy, incomplete work and stale evidence cannot be bypassed.
  Supporting foundations are scheduled when needed to regain eligibility.
- Optional coordinated programming chooses the least recently practiced eligible
  selected block that fits today, using workout dates, not backup array order.
  It keeps block-specific unfinished queues and movement-specific prescriptions.
- Shared demand spacing, global heavy/density spacing, weekly limits, absence/re-entry,
  low readiness and optional deloads apply. Missed days add no catch-up work.
  Whole prescriptions fit the time budget or are deferred; reduced/incomplete work
  earns no ordinary progression credit. Load increases remain explicit and owned.
- The expandable decision panel explains selection, blocked alternatives, emphasis,
  clean-exposure goals, reduced practice and cycle endpoints. Observed cadence can
  flag a rotation larger than recent frequency can sustain before re-entry.
  Its 56-day sample/formula are app heuristics, not physiological/source rules.
- Complete overview, freely accessible set logging, integrated/rest timers,
  adjustable duration, offline research and saved training history remain intact.
  V31/V32 continue in separate storage/interface.

## Data protection

JSON backups include active drafts, sets, stage, notes and paused/running clocks.
Validation rejects malformed/incompatible/duplicate data before changing storage;
older V33 backups without a draft remain supported.

A write-ahead rollback journal protects history/draft replacement and completion.
Failed saves retain the draft for retry; interrupted transactions recover on reload.
If rollback fails, the prior snapshot remains readable and writes are blocked.

Updated clients require a lifetime browser Web Lock before editing/recovery.
Other tabs are read/export-only, follow saved data and never roll back the owner's
transaction. Close the owner and reload another tab to resume the latest draft.
Raw-value checks and storage events block stale/unexpected overwrites. Without
Web Locks on a supported secure origin, the app remains read/export-only.
See PERSISTENCE.md for old-client, physical-storage and device limitations.

## Verified in this recovery

- All **98 named Node tests**, engine assertions and legacy smoke passed.
- Real Chromium: 36 coordinated workouts over multiple simulated months, including
  independent families, incomplete work, missed month, pain, short sessions,
  equipment loss/return, skill regression/reconfirmation, low readiness and offline
  history. Full work that does not fit is refused; reduced work does not promote.
- Four actual saved workouts verify cadence/absence feedback, same-day spacing,
  normal/re-entry goal explanations, and clearing the warning by selecting fewer
  blocks without changing history.
- Real multi-tab ownership/import/save guards, live draft/set/timer view, in-flight
  journal reader, close/reload handoff, duplicate prevention, external/synchronous
  stale checks, unsaved export, offline ownership and unsupported-lock mode pass.
- Backup fault injection: running/paused clocks, malformed/duplicate rejection,
  journal/second-key/discard/save failures, rollback, retry, interrupted commit,
  failed startup recovery with blocked writes, later recovery and offline reload.
- Baseline-to-current worker upgrade preserves raw saved keys/draft byte-for-byte
  and continues the old workout offline under mobile emulation. Timer lifecycle
  and free set-logging browser regressions pass.
- 30 quotation/hash anchors and the complete 720-source coverage/registry check pass.
  The 23-system matrix remains four implemented scopes, twelve partial, seven missing.

Earlier checkpoints also verified the complete push-up wave, get-up/club pathways,
13 loaded-hinge workouts and 44 snatch workouts. Those longer suites remain in the
repository; they were not all rerun during this smaller recovery increment.
Browser histories test software using self-reported input, not training efficacy.

## Next priorities

1. Further composition/workload interaction tests and clearer rotation/pattern
   coverage. Current demand groups and cadence are conservative app choices,
   not a complete Tetris curriculum or individualized fatigue model.
2. High-value foundational gaps: complete ground transitions/traveling quadruped
   work, then reviewed intermediate club pathways. Loaded two-hand hinge is done;
   unilateral/stance variations remain separate. Avoid low-value exercise additions.
3. Accessibility and release reliability, including broader upgrade/ownership
   scenarios and physical Android/installed-PWA checks. Keep future Capacitor
   compatibility; no APK packaging until core release readiness.
4. A truly fresh Codex-task/snapshot restoration check when tools support it.
   This executor was restored with its workspace; that is not proof that every
   future task/environment retains local edits or authentication. GitHub is the
   persistent checkpoint.

## Reproduce

Run root `*.test.cjs` with Node plus `node v31-smoke-test.cjs`.
Representative real-browser suites: `tests/multi-tab.py`, `tests/backup-restore.py`,
`tests/composition-feedback.py`, `tests/composition-histories.py`,
`tests/service-worker-upgrade.py`, `tests/hinge-pathway-histories.py`.
Run `tests/research-provenance.py` and `tests/curriculum-coverage.py` for research.
Python Playwright and `/usr/bin/chromium` are available; browser/socket commands
use the supported execution permission flow. No build/dependency install is needed.
Read DEVELOPMENT-LOG.md and NEXT-CONTINUATION.md before editing.

## Development web preview — live

Public URL: https://zwbeam.github.io/strength-lab-preview/
Verified source e62542b3d5f81923bf7a9025f72243972e300121, deployment
08b6544f29885370ee3f03f08e038271534b2c33. The owner enabled Pages on the separate
preview repo/branch. Actual public HTTPS tests pass in Pixel 5 Chromium emulation:
76 assets, version/manifest/storage identity, mobile layout, full overview,
timers/logging, progress/settings/library and offline reload/source reading.
Not physically tested on Android. No further user setup is required.

The original live app's assets, Pages/main-root settings and main SHA remain
unchanged. No production release or APK was made. Future updates use the guarded
scripts/publish-preview.py, followed by tests/preview-url.py against the expected
source SHA; development pushes alone do not auto-publish. See PREVIEW.md for phone
access/update instructions. Later test/doc/tool-only commits do not change the
app version until explicitly published.
