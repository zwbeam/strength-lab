# Strength Lab development log

## 2026-11-05 — Source-scoped programming engine

Preserved branch history through `374967f`. Reviewed source lessons #3, #120,
#228, #288, #366, #403, #410, #411, #548 and #561, plus the previously reviewed
volume/warmup/stall material. Added `research/programming-rules.json` with eleven
verified quote anchors, URLs and normalized-text hashes. Source examples and
configurable app safeguards are separated explicitly.

Implemented optional snatch EMOM volume/density and double-kettlebell strength
blocks, club timed practice, heavy/light waves, explicit supported-cycle and
owned-load choices, prerequisite gates, stall alternatives, deload and recovery
scheduling. Complete prescriptions are fitted within the session duration;
missed days never generate catch-up volume. Existing ABC history remains on
its original policy identity. New profiles record their identity and provenance.

Fourteen programming-history tests pass, including full snatch cycles, multiple
weeks of double-grind and heavy/light work, failures, side differences, recovery,
missed weeks, durations, owned pairs and backup roundtrips. Existing engine,
completion, recovery, backup and legacy suites also pass. Eleven quote/hash
checks pass. Application wiring and final upgrade verification follow in a
separate focused commit.

## 2026-11-05 — Application programming and history validation

Wired source blocks, parameter controls, prerequisite confirmations, cadence and
numeric side logging, phase/load decisions and recovery scheduling into the real
application. Added per-block carryover, protected active drafts from configuration
changes, validated pair inventories, and preserved default policy identities when
explicit defaults are saved. Exposed own heavy-rep and club set/rest parameters.

Additional regression work corrected heavy sizing against completed rather than
future light work; retained the wave cycle count on the heavy lane; distinguished
incomplete work from completed-but-poor technique in stall alternatives; and
prevented adapted recovery parameters from claiming exact source example support.
Density prescriptions cite #410, volume cites #411. Forty-one named engine/recovery/
completion/backup tests now pass, plus existing engine and legacy assertions.

The real app passed 44 successful source-cycle exposures across about 19 simulated
weeks, followed by partial work, poor technique, imbalance, pain, a missed month,
re-entry and calendar spacing. A separate UI history passed six ABC sessions with
heavy/light work, matched-pair/skill gates, 20-minute movement carryover, custom
club settings and draft/equipment guards. Six existing browser DOM suites,
root/subpath offline checks and provenance checks also pass. These are software
simulations using self-reported input, not claims of real training efficacy.

## 2026-11-05 — Upgrade verification and environment boundary

After the training implementation, completed the previously outstanding
service-worker upgrade check from committed baseline `374967f` to the new app.
The test uses a temporary checkout copy and Chromium Pixel 5 emulation. Existing
V31/V33 saved keys and an active rest/workout draft remained byte-identical through
the upgrade; offline reload and saving the old partial workout succeeded.
Physical Android installation remains untested.

Current runtime status still identifies the original onboarding environment and
source version. No fresh-task creation tool is exposed, so cloud snapshot
restoration remains unverified. Browser tests are not substituted for that claim.
No additional authorization or setup was requested; no branch was pushed, merged
or force-pushed, and no release artifact was generated. Full raw source history
and prior development checkpoints remain ancestors of this branch.

## 2026-11-05 — Remote persistence and curriculum foundations

Pushed `development/reconciliation` through the existing Git proxy. A separate
fresh checkout recovered `fe744c4`, passed `git fsck --full` and all 22 programming
tests; remote main stayed at `4cb58d8`. PERSISTENCE.md distinguishes this verified
GitHub recovery from the still-unavailable fresh Codex task/snapshot test.

Screened all 720 full transcripts into a reproducible 23-system curriculum matrix.
Title/full-text matches are explicitly discovery candidates, not reviewed rules.
Added five close-read quotation/hash entries for #423/#658 get-ups, #578/#581
single-arm club volume/rest and #543 prior foundation. Sixteen provenance entries
now match the verified corpus.

Implemented the get-up 3–10 total-minute goal and single-arm inside/outside/shield
continuous 4–20×5 foundation cycles. A shared movement/skill/block registry feeds
the library, source links, prerequisites and generator. Get-ups log actual total
seconds separately from side rep counts, including the source's one-extra-weak-
side allowance. One-bout recovery reduces duration. Club rest runs between
movements, not sets. Existing profiles, policy identities and stored records remain.

Ten new engine tests and actual HTTP histories passed: 16 successful get-up
exposures plus five adverse/recovery cases; 34 successful three-movement club
exposures plus one interrupted case (102 successful club movement records).
Equipment/skill gates, eight-plus-week goals, weak-side imbalance, continuity,
pain/re-entry, missed weeks, duration deferrals and timer persistence were exercised.
The existing six DOM suites, root/subpath offline checks, worker upgrade, existing
engine/backup/recovery/legacy suites also pass. The library test needed an explicit
wait for asynchronous transcript loading; it then passed with exact source text.

No Android packaging or release work was introduced. The runtime remains pure
browser JavaScript with relative bundled assets, compatible with later Capacitor
integration. Physical Android and complete advanced curricula remain outstanding.

Final UI consistency review removed two-hand timed-practice controls from
single-arm continuous-volume settings. The engine already ignored those controls;
the form now exposes only the correct progression choices. A real HTTP library/
settings test verifies this separation and the prerequisite teaching links.

A second independent fresh checkout recovered curriculum checkpoint `2817a3f`
from GitHub and passed object verification, the 22 programming and 10 curriculum
tests, 16 provenance checks and the full 720-source coverage/registry check.
Remote persistence is verified; fresh Codex task/snapshot restoration is still a
separate unavailable check. The remaining curriculum and exact continuation prompt
are documented in DEVELOPMENT-STATUS.md and NEXT-CONTINUATION.md.

## 2026-11-05 — Reviewed practice pathways and foundational bodyweight systems

Verified local HEAD against the fetched remote development branch before edits;
main remained unchanged. Read the requested breakdown and intermediate teaching
sources plus #704 unloaded hinge and #609 push-up programming.

Implemented four get-up breakdowns and five intermediate club movements using
shared skill/practice dependencies. Recent clean parent work and explicit skill
review are both required; supporting movements are generated when needed. Added
maintenance of established evidence through active practice, with transitive
pain/skill/load guards. One-set recovery now reduces reps. Exact intermediate
numbers and gate thresholds are identified as app defaults, not invented source
prescriptions.

Continued beyond those pathways with unloaded hinge preparation and push-up EMOM
volume. Added explicit bodyweight zero-load support without weakening weighted
movement validation, conservative baseline entry and deliberate cycle restarts.
A technique-correction record may be performed but is never progression-eligible.

Thirteen pathway and seven bodyweight engine tests pass alongside the prior 51
named tests. Actual HTTP histories passed the generated get-up and club pathways,
including skill review, incomplete work, equipment loss, missed-month re-entry,
maintenance and transitive pain holds. The bodyweight UI passed a complete
42-exposure push-up wave, hinge quick logging at zero load, baseline review,
technique/pain/re-entry and offline checks. Twenty-six rule quotations/hashes
match the original verified transcript corpus. Coverage remains scoped rather
than claiming a complete interpretation of 720 lessons.


## 2026-11-06 — Recover interrupted work and protect active-workout backups

Confirmed remote development HEAD `b07a0e7` includes both interrupted movement
commits; retained all history. The backup changes survived uncommitted, while
the proposed browser test was absent. Reviewed the implementation before testing.
Completed draft validation/export/import, stable session/draft identities,
rollback/retry and a write-ahead journal for interrupted paired writes. Added
blocked-write recovery mode when storage also fails during rollback. Discard,
reset and restore preserve the previous data on transaction failure.

Passed all 75 named Node tests and existing engine/legacy assertions. Created
and passed real Chromium `tests/backup-restore.py`, including active sets/paused
timer restoration, malformed and already-saved draft rejection, second-key write
failure, save removal failure, safe retry, simulated interrupted commit, failed
startup rollback, successful later recovery, and offline reload. Corrected the
bodyweight history restore test to wait for the actual asynchronous import.


## 2026-11-06 — Ground foundations after the persistence checkpoint

Pushed and verified backup checkpoint `6c3df46`; main remained `4cb58d8`.
Close-read #84/#98/#100 and the ground/quadruped context in #102/#554. Added
2-hand to 1-hand hip-drop practice and bear-squat mobility, using shared explicit
skills, recent supporting evidence, source teaching links, selectable block,
editable practice doses and existing recovery/complete-work rules. Numeric hip-drop
rep practice and set/rest/exposure choices are labeled app defaults; source-timed
examples are not misrepresented as universal prescriptions. No loaded get-up,
crawl or complex flow competency is inferred.

Five new engine tests and 15 actual generated UI sessions pass, covering
incomplete work, explicit review, successful progression, short duration, no
equipment, stale prerequisite requalification, parent pain, edited doses and
offline reload. Integration testing caught and corrected a missing shared
settings-control condition before commit. All 80 named Node tests pass alongside
engine and legacy assertions; provenance now verifies 29 quotation/hash anchors.
The matrix was regenerated against all 720 sources and the runtime registry.

## 2026-11-06 — Cross-program recovery and import integrity

After the ground checkpoint, found that the new ground family lacked shared
recovery demands. Added conservative lower-body/shoulder overlap so configured
spacing also respects ground work across other blocks, including partial and
recovery sessions. Every registered movement now has a demand mapping. These are
app scheduling defaults, not source-specific fatigue measurements. Close-read
#548/#561 for composition/recovery context without importing personal injury
examples as a universal rehabilitation protocol.

Fixed unavailable-workout guidance: pain, paused training, prerequisites, scheduling
and missing equipment no longer misleadingly suggest extra time/lower readiness as
a cure. Duplicate session IDs, originating draft IDs and movements are rejected
on backup import, preserving prior data and preventing multiplied evidence.

82 named Node tests pass. Real browser fault injection also covers running-timer
roundtrip, failed discard, journal-write failure and duplicate-history rejection.
The generated ground UI verifies spacing and proper blocked-workout guidance.
Recovered bodyweight/pathway histories, original snatch/get-up/club histories,
programming controls, all six timer/focus/library DOM suites, offline root/subpath
and worker upgrade checks passed in this task. Remaining limitations and priorities
are consolidated in DEVELOPMENT-STATUS.md.
