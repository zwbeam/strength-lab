# Strength Lab user experience reviews

## Permanent process — approved in user request, review 1

Build a coherent milestone → automated/browser verification → publish the separate
preview when access permits → document changes/limits → pause for user feedback.
Passing tests does not establish satisfactory usability. Do not begin another
major interface/workflow redesign before the next user-review checkpoint.

## Review 1: approved requirements

- Repair the frozen/noninteractive active-workout timer in the actual interface.
- Settings timer modes: Manual (initial default), Automatic, Hybrid. Keep active
  workout state intact when changing the preference. Preserve free logging/overview.
- Rename Atlas to Learn. Primary browsing: Exercises by equipment/family and focused
  Pathways from the same movement registry. Keep research internally, not as a primary
  raw-transcript archive.
- Practical source-grounded instruction, explicit coverage gaps, one/two exact source
  video links where mapped, and no invented timestamps.
- Educational access remains open regardless of training eligibility. No automatic
  technique certification from repetitions. Programming remains explicitly incomplete.
- Preserve main/live app/data; publish only the isolated DEV preview after verification.

## Reported problem: active workout timer

**Reproduced:** a real Pixel 5-sized touch workflow entered working sets with
`draft.clock === null`. The visible interval showed 00:00; its only controls were
+30 sec and Skip/clear. +30 did nothing when no clock existed. The number itself
was a noninteractive strong element. Three elapsed seconds/tapping +30 left 00:00.
The separate session budget counted, making the two displays easy to confuse.

**Why previous checks missed it:** timer tests explicitly started a warmup timer
or logged a set before examining rest controls; some asserted labels/control
presence without elapsed time. They never tested tapping the idle active-workout
face or adding time with no clock. They also did not verify expiry replaced stale
Pause controls without a user-triggered render.

**Implementation candidate, awaiting user review:** the interval face is a large
semantic touch button with an explicit Start/Pause/Resume/confirmation control.
Manual prepares the next interval without starting it; Automatic advances pacing;
Hybrid waits before another exercise. Work durations for rep-based sets are
labeled app estimates. Continuous club practice has no invented inter-set rest.
No timer mode logs sets, cadence confirmations, skills or progression credit.
Mode is captured in each new draft; settings changes apply to later workouts.
Existing paused/running clocks and V33 backups remain compatible. Wall-clock
reconciliation handles throttling/frozen pages and offline reload. The timer
is not sticky over the exercise overview. The session budget is labeled advisory.

**Verified locally:** seven controller tests, three rendered touch-mode workflows,
real browser freeze/resume, offline draft/mode preservation and free set logging.
Physical Android behavior still needs the user's review. Authenticated GitHub
currently rejects credentials (401); local checkpoints must not be reported as pushed.

## Review questions after the milestone

- Does the timer now start reliably by tapping the face or Start interval?
- Is Manual a useful default? Are rest cues and Hybrid confirmations understandable?
- Can you find an exercise and understand its setup without opening a transcript?
- Do the focused pathway/status explanations make the next learning step clear?
- Are the video links easy to open in Chrome/YouTube on your Android phone?

Record user feedback and resolutions below before any further major redesign.

## 2026-11-06 — UX review 1: Learn milestone

Replaced primary Atlas/archive navigation with Exercises and focused Pathways,
both derived from the 31-movement registry. Practical source-reviewed outlines
include setup, steps, bracing, corrections and explicit coverage limitations.
29 movements have one/two exact corpus video mappings; suitcase carry and front
squat remain unmapped. Get-up/push-up programming videos and partial technique
coverage are labeled honestly. No timestamps were invented; external playback on
a physical phone has not been verified. Provenance checks validate 29 exact quotes
and 36 source hashes against the indexed corpus.

Maps separate enforced practice prerequisites from educational complexity and
combination links. Four statuses use actual eligibility/history or explicit user
familiarity confirmation; repetition never certifies mastery. Blocked lessons stay
readable, including in read-only tabs. Familiarity does not bypass programming.
Volume/density/load explanations preserve the existing engine and distinguish app
defaults. The complete offline corpus remains secondary evidence, not primary UI.
This is a review candidate, not a claim of complete instruction or programming.

## Published review candidate

Source 7c6f2c0 is live at https://zwbeam.github.io/strength-lab-preview/.
The authenticated GitHub connection recovered and both local milestones were
pushed normally. Public HTTPS/mobile-emulation checks passed all 79 assets,
workout flow, Learn and offline reading. Earlier 401 notes describe the temporary
blocker, not the final publication status. No physical Android testing or user
approval of the new interface has occurred. Awaiting feedback on the questions
above; do not start a new major redesign before that review.

## Review 2 — approved commission: training notebook

This commission authorizes the Train/history rebuild after review 1. Preserve
Learn and the training engine. The user explicitly requests a persistent compact
sticky timer; this supersedes review 1's nonsticky implementation candidate.

Approved requirements: ordered cycle without mandatory weekdays; complete session
preview; normal duration with one-session duration/readiness overrides; compact
prefilled log with optional set editors; one explicit final affirmation; accurate
partial work; instruction overlays; reversible historical corrections with
progression reconciliation; offline/backup/atomic multi-tab reliability. Charcoal
and teal identity, source distinctions, original production app and history stay.

### Implemented candidate, awaiting Android review

- Train opens an ordered current cycle, with recent records and navigable
  provisional upcoming workouts. Future previews use current training evidence;
  they do not promise automatic load/skill advancement. Only next recommended
  work can start, so inspection cannot bypass recovery or prerequisites.
- Selected session shows explicit collapsible preparation, complete prescriptions
  and method/rest information. Actual engine adaptation is explained. Duration
  override does not change Settings; Feeling great adds no extra work.
- Active view is a single compact notebook. Targets are prefilled; Edit reveals
  set-specific values, side differences, timing/rest, notes and add/remove/bulk
  performed/unperformed controls. Optional checkoffs remain, never mandatory.
- Sticky timer uses the prior repaired wall-clock controller and modes. Instruction
  opens over the unchanged workout. No timer event claims performed physical work.
- Final confirmation distinguishes completed targets/modifications and partial
  work. A partial finish saves only explicitly performed sets. A completed finish
  is a self-report of non-skipped sets, matching sides/cadence/continuous work
  unless edited. Full get-up counts per side must still be entered, not invented.
- Progress exposes set-level actuals and corrections with prior versions and a
  restore action. Engine replay updates future targets and eligibility. Correction
  withdraws affected pending load selections; it does not rewrite past workouts.
- Preparation doses/cooldown are documented app defaults. #670 supports pattern
  priming, not this exact routine. Learn/curriculum coverage is unchanged.

### Evidence and review boundaries

Pixel 5 Chromium touch acceptance passed: cycle inspection, 45→30/Pretty beat,
real changed prescription, sticky elapsed countdown, instruction return, one
confirmation, final-set edit, correction/replay/undo, backup and offline reload.
Fault tests passed failed saves/corrections with rollback/retry, partial-draft
restoration, add/remove sets and read-only second-tab protection. This establishes
software behavior; it does not establish satisfactory UX or physical Android
reliability. Additional existing long-history regressions/publication status are
recorded in the development log and PREVIEW.md.

Please review: Is the compact page readable? Are normal versus partial final
confirmation and bulk unperformed controls unambiguous? Is timer visibility useful
without covering work? Do instruction overlays return to the right place? Can you
correct a set days later and understand its effect on the next workout?

Pause for this feedback before a new major interface/workflow redesign.

### Review 2 published checkpoint — 2026-11-07

Live: https://zwbeam.github.io/strength-lab-preview/ · banner 1e32b29.
Source 1e32b29363a247946ce4bb9c0b932b0a50bbc183; deployment
79c65b8165a2311a6ca6bf993b340b878486901b. Actual HTTPS Pixel 5 acceptance
passed complete adjustment/timer/log/history correction/replay/backup/offline flow
and all 80 runtime assets. Original main/Pages/live file fingerprints unchanged.
127 named Node cases, existing browser/history/failure regressions and source
checks passed. User/physical Android approval remains outstanding. Pause here.
