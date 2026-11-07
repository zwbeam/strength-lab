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

## 2026-11-06 — Independent remote recovery checkpoint

Normally pushed `d99a153` and verified the GitHub ref; main remains `4cb58d8`.
A separate clone recovered that exact development commit and passed Git object
verification, all Node suites, 29 quote/hash anchors, the 720-source registry
check, and real Chromium backup and ground-history tests. No working-tree files
were copied into the clone. Fresh Codex-task creation is unavailable; its actual
environment restoration/authentication cannot be claimed. See PERSISTENCE.md.

No partially implemented changes are being left behind. The next priorities are
richer cross-program composition, broader release/accessibility/storage stress
checks (including multi-tab concurrency), then reviewed remaining foundational
pathways. Continue from the latest remote development branch using
NEXT-CONTINUATION.md. No user setup is currently required.

## 2026-11-06 — Coordinated programming checkpoint

Verified clean local and remote `86985ee`, read current status/rules/coverage and
close-read #548/#288/#578. Audited the single-block planner: movement cycles and
scoped carryover existed but no multi-block coordination. Added opt-in selection
across existing blocks using least-recent actual work, eligibility, whole-target
time fitting, supporting practice, shared demand spacing and global hard-work
spacing. Policies, source-specific rest and progression remain independent.
Added Settings controls and a compact decision panel; saved sessions identify
coordinated versus manual programming. All scheduling choices are labeled app
defaults, distinct from the reviewed sources.

Eight new engine tests pass, including 48 generated workouts across four families
and multiple months. Actual Chromium passed 34 saved workouts across four blocks,
partial work, missed-month re-entry, shorter sessions, pain, decision explanations,
reload/offline and independent history. Existing programming-control browser suite
and all 90 named Node tests pass. Multi-tab reliability is the next active task.

## 2026-11-06 — Exclusive writer and stale-state protection

Added lifetime browser Web Lock ownership before storage recovery. Readers never
roll back an active writer's transaction and cannot mutate/import. Read-only tabs
follow saved state/drafts, retain library/export access and explain close/reload
handoff. Raw-value guards and storage events stop unexpected/stale overwrites.
Unsupported lock environments remain read/export-only. Added an explicit duplicate
originating-draft check at workout save, including older inconsistent snapshots.
Generic settings/history saves now use paired transactions and restore saved state
on failure; timer auto-writes are suppressed in read-only/conflicted/recovery mode.

Real `tests/multi-tab.py` passes ownership, active journal readers, set/timer view,
failed read-only import/save, close/reload handoff, duplicates, external changes,
synchronous stale checks, backup, offline and unsupported-browser cases. Existing
backup failure and mobile-emulated worker-upgrade suites pass. All 90 named Node
tests and six DOM suites pass. DOM fixtures now have a localhost test origin for
real Web Locks while retaining their explicitly simulated storage. No fake lock
fallback was added to production. Details and older-client limits are in PERSISTENCE.md.

## 2026-11-06 — Foundational loaded hinge pathway

After pushing coordinated programming `b05b82c` and writer protection `ea80b41`,
close-read #704 and added a two-hand deadlift registry entry/profile/block. It
uses explicit loaded technique plus recent unloaded supporting evidence, shared
recovery and owned-load review. Loaded set/rep/rest choices are configurable app
defaults; the source's 2–3×10 example is correctly retained as unloaded only.
No existing swing/ABC policy or progression was altered.

Five engine tests and 13 actual generated/saved UI workouts pass: incomplete
foundation work, explicit review, short duration, complete loaded cycle, owned
25% load increase, stale-parent requalification, pain and offline history.
The changed-load test verifies that stale evidence is regenerated rather than
silently reused. 95 named Node tests and engine/legacy assertions pass. Thirty
quotation/hash anchors and the regenerated 720-source coverage/registry check pass.
The hinge coverage row remains partial; unilateral/stance pathways are unfinished.

## 2026-11-06 — Executor recovery and chronological composition

The environment returned from executor failure. Verified local and remote HEAD
at `a68b180` and ancestry of `b05b82c` / `ea80b41`; main remains `4cb58d8`.
The three reported uncommitted files survived. Reviewed the chronological-history
change rather than reconstructing it: composition now sorts a filtered copy by
date before selecting the least recently practiced block. Raw history is unchanged.
Nine composition and five hinge tests plus 30 provenance checks pass. The extended
browser test remains under review; its first failure assumes a whole advanced
bear-squat prescription fits a 15-minute session. No unverified test is committed
with this small recovery increment.

## 2026-11-06 — Recovered adverse composition histories verified

The surviving browser extension is now reviewed and passes 36 real generated
workouts. Its failing expectation was a test error: the full four-bout bear-squat
target does not fit seven main-work minutes in a 15-minute session. The corrected
sequence verifies that refusal, deliberately selects low readiness for reduced
non-progressing work, then restores 45 minutes before checking full weighted work.
Equipment loss/return, revoked/reconfirmed skills, pain, missed-month re-entry,
independent cycles, saved state and offline reload pass. Real multi-tab and backup
fault-injection suites also pass in the recovered executor. `8e35d01` was pushed
normally; the three prior reported commits are confirmed on origin.

## 2026-11-06 — Manageable rotation feedback

Added observed-cadence feedback to the existing expandable decision panel. With
at least four training days in a 56-day sample, the app compares estimated block
return time with the configured absence threshold and suggests fewer active blocks
when the selection is likely to keep returning through re-entry. This is explicitly
an app planning heuristic; it changes no prescription, gate or progression credit.
The panel now explains normal clean-exposure goals, reduced non-progressing work
and cycle endpoints, with a concise rotation-review summary when needed.

Two additional engine tests and a four-workout real-browser workflow pass. The
workflow checks the 24-day estimate, actual reduced re-entry, preserved same-day
recovery spacing, normal clean-exposure feedback, and a 12-day estimate/no warning
after reducing to two blocks without altering history. All 98 named Node tests,
engine/legacy assertions, 30 provenance anchors and the 720-source registry check
pass. Offline worker upgrade, timer lifecycle and free set logging also pass in
this restored executor. Earlier small increments were pushed separately.

## 2026-11-06 — Independent recovered-source verification and handoff

Independently cloned origin into `/tmp/strength-lab-recovered-checkout-s910hab1`
and recovered `7e4a04914c0306830bf27f433183a421d5f7daf8`. Git object verification,
all Node suites, 30 provenance anchors, the 720-source registry check, actual
cadence workflow and real multi-tab suite passed from that clone. No local working
files were copied. Restored executor functionality and remote persistence are
verified; a genuinely fresh Codex task/snapshot is still a distinct unavailable
check. Main remains unchanged.

Consolidated status and continuation instructions to remove stale claims that
composition, multi-tab protection and loaded hinge practice were unfinished.
No partial implementation is being left behind. Further workload/coverage tests,
accessibility/release reliability and reviewed foundational ground/quadruped or
intermediate club pathways are next. No user setup is required; no main merge,
force-push, release or APK was produced.

## 2026-11-06 — Isolated Android-friendly preview preparation

Verified HEAD/origin at `d5603e8` and main `4cb58d8`. Read status/log/continuation
and inspected both branch trees: no deployment workflows, CNAME or documented
hosting route. Existing main contains the older V32 static application. GitHub API
and the likely Pages hostname returned proxy 403; actual Pages settings, account
permissions and public URL cannot yet be verified. Saved a narrowly scoped network
draft for api.github.com and zwbeam.github.io; backend confirmed saved and requires
user review/save/Publish. No Pages source, live deployment or main change was made.

Implemented a deterministic preview builder reading committed runtime assets.
Generated output has a DEV banner/SHA, distinct manifest identity, V33 and legacy
storage keys, writer lock and worker cache prefix/scope. The live app's broad
strength-lab-* cleanup cannot delete sl-dev-preview-* caches. The builder rejects
nonempty/inside-checkout destinations and changed isolation contracts. Production
app.js/engine.js/training features remain unchanged. Added public-URL verification
tooling, intentionally not claimed as run because no deployed URL is accessible.

Passed all 98 named existing Node tests plus engine/legacy assertions; representative
root/subpath browser smoke; and Pixel 5-emulated preview coexistence at
/strength-lab/dev-preview/ with 76 assets, version/manifest, no horizontal overview
overflow, settings/library/progress, timers/logging, offline source reading and
separate live data/locks/caches. Both preview and live worker upgrades preserve
isolation; preview test history survives its update. Original main runtime files
and seeded live storage remain unchanged. This is local mobile emulation, not a
physical Android test or proof of public deployment.

PREVIEW.md and continuation/status now identify the concrete remaining action:
apply the saved network draft, inspect actual hosting settings, publish through a
route preserving the live app/update mechanism, then verify the real HTTPS URL
with tests/preview-url.py before handing the user a phone link. No release/APK,
force-push, main merge or automatic deployment workflow was created.

## 2026-11-06 — Preview hosting access restored

The newly published environment allows api.github.com and zwbeam.github.io.
Verified source HEAD/origin `1a02f2d`, GitHub owner zwbeam, and existing Pages at
https://zwbeam.github.io/strength-lab/ serving main at repository root. GitHub
metadata reports this source repository is public (earlier private-repo assumptions
were not verified). Captured live index/app/worker/manifest SHA-256 fingerprints.

An additive preview under that branch source would require changing main or the
existing deployment. Prepared a guarded publisher for a separate free GitHub Pages
repository, zwbeam/strength-lab-preview, on its own preview branch. It writes no
source-main or source-Pages settings and validates ownership/configuration/managed
files before updates. Actual publication and public verification are the next steps;
this entry does not claim a live preview yet.

## 2026-11-06 — Preview publication blocked by repository-creation permission

The isolated Android-sized coexistence suite passes again. Pushed publisher
checkpoint `e795c65` normally to source development. Actual creation through
POST user/repos returned GitHub HTTP 403: Resource not accessible by integration.
No preview deployment was claimed. Queried installed applications: the active
chatgpt-codex-connector has all-repository selection, so the owner only needs to
create an empty public strength-lab-preview repository; no repeated network setup
or credential sharing is required. Existing Pages/main stayed untouched.

Improved the publisher to fetch its default source tracking ref before building
(explicit development pushes can leave local tracking refs stale), and explain
the owner action clearly on integration creation denial. Four mocked guard tests
pass for creation permission failure, wrong owner, private target and unfamiliar
branch; they verify stopping without source writes. Rechecked real live asset
fingerprints and source Pages/main after the failed attempt: all unchanged.
Updated preview/status/continuation docs with the precise next action and the
separate free hosting route. Actual public HTTPS verification remains pending.

## 2026-11-06 — Preview uploaded; owner Pages setting required

The owner created the public preview repo. Verified access and empty branch list,
then uploaded all 77 generated files on preview as f482bac, built from source
613c408. First push automatically set the preview default branch. The original
publisher unnecessarily tried to reassert that setting using stale metadata and
received 403; removed that administrative write. Direct first-time Pages enablement
also returned integration 403. Installation permissions confirm contents/workflows
write but no administration/pages access. The official configure-pages action
explicitly says normal GITHUB_TOKEN cannot enable Pages, so no token workaround
or new workflow was attempted. Owner Settings → Pages → Deploy from branch →
preview / (root) → Save is the one remaining setup action.

The publisher now uploads/updates content without any administration/Pages-write
calls, reports an explicit owner setup requirement when disabled, and retains
source-main/Pages invariance checks. Four publisher guard tests pass. Android-sized
coexistence tests passed again. Rechecked actual live index/app/worker/manifest
fingerprints: unchanged. Public HTTPS preview verification still awaits enablement;
network and repository creation must not be requested again.

## 2026-11-06 — Preview update path verified

Uploaded source e62542b3d5f81923bf7a9025f72243972e300121 as normal deployment
commit 08b6544f29885370ee3f03f08e038271534b2c33 on the separate preview branch.
No administration/Pages-write calls were required. Source main and Pages settings
passed invariance checks. Corrected the managed-file guard to include sw.js itself,
which is intentionally not in its own precache inventory. The real repeat update
succeeded without force-push or lost deployment history. Pages remains disabled;
owner enablement in the preview repo settings is still the only required action.

## 2026-11-06 — Public Android-friendly preview verified live

The owner enabled Pages on the separate preview repo/preview branch. GitHub build
08b6544f29885370ee3f03f08e038271534b2c33 completed and the public metadata returns
source e62542b3d5f81923bf7a9025f72243972e300121. Live HTTPS URL:
https://zwbeam.github.io/strength-lab-preview/.

The first browser probe attempted direct DNS, unavailable in the managed proxy
network. Updated only the public verifier to inherit HTTPS proxy and configured
CA trust, leaving TLS verification enabled. The rerun passed against the actual
public URL: all 76 assets, SHA/banner/manifest identity, isolated storage/lock,
Android-sized layout without overflow, complete workout overview, timer pause/
resume, set logging, saved Progress, Settings/library and offline reload/source
reader. This is Pixel 5 Chromium emulation, not physical Android testing.

Original live app index/app/worker/manifest fingerprints, main SHA 4cb58d8 and
original Pages main/root configuration remain unchanged. No release, APK, force
push or main merge was created. All owner setup is complete. Updated preview,
status and continuation docs with the verified link, exact version and normal
future publishing procedure. No additional user authorization/setup is needed.

## 2026-11-06 — UX review 1 timer repair, local milestone

Read the pasted UX request and current status/log/continuation/coverage/rules.
Public GitHub API confirms source checkpoint fb3db7f; authenticated Git/CLI access
now returns invalid credentials/401, so no remote-write success is claimed.
Reproduced the reported rendered timer failure with Pixel 5 touch: work entry
cleared clock to null/00:00, exposed no Start control, and +30 silently did nothing.
Earlier tests first started warmup or logged sets and missed this idle state.

Added a pacing-only session timer with Manual default, Automatic intervals and
Hybrid exercise confirmations. The display is an actual touch control; explicit
primary controls and +30/skip remain available, expiry rerenders controls, and the
nonsticky panel preserves the full overview/free logging. Wall-clock deadlines
handle frozen pages/resume. Each new draft captures its mode; preference changes
only affect later workouts. Continuous club bouts avoid inter-set rest; timers
never fabricate completed sets or cadence/skill confirmations. V33 validation
accepts the new preference/draft fields while preserving old drafts.

Seven new controller tests and actual touch workflows for all three modes pass,
including timer changes, background freeze/resume, preference snapshots and offline
reload/logging. Existing Node suites pass. Existing timer fixtures now load the new
runtime module; old automatic-rest tests explicitly select Automatic while Manual
skip/idle assertions reflect the requested behavior. Upgrade fixtures copy the
actual new runtime HTML/module assets. USER-EXPERIENCE-REVIEW.md records approved
requirements, the diagnosis/test gap and review checkpoints. GitHub publication
remains dependent on refreshing the existing connection; no credential sharing.

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

### UX review 1 publication and verification

GitHub credentials recovered without replacing tokens or repeating owner setup.
Fetched remote fb3db7f and pushed timer 2d97220 and Learn 7c6f2c0 normally.
GitHub API confirms 7c6f2c0070840db3da4a1c813ae57e1bb8411e92 on development.
Published that source to preview deployment
2b5e4a71c1b62ae8287c2edb1625a358af809f05. Pages completed; actual HTTPS
https://zwbeam.github.io/strength-lab-preview/ passed Pixel 5 Chromium emulation
with all 79 assets, identity/storage separation, layout, full overview, timers,
logging, progress, Learn, Settings and offline source reading. Initial public
check correctly rejected the stale previous build while Pages was still building.
Original main and Pages configuration were verified unchanged by the publisher.

All 111 named Node tests plus engine and V31 smoke checks pass. Browser tests
passed for all six existing DOM workflows, timer touch modes/frozen resume,
Learn/status/map/video targets, curriculum links, root and subpath smoke,
programming controls, backup rollback/retry, multi-tab writer protection,
service-worker upgrades and preview isolation. Exact source hashes/quotes pass.
Video URLs are verified against corpus metadata; no physical Android or external
YouTube playback verification is claimed. Pause for user feedback before another
major interface redesign, as requested. See USER-EXPERIENCE-REVIEW.md.

The strengthened public verifier also tapped the active-work timer face, observed
real elapsed countdown, paused it and verified that pacing logged no sets. The
original live root/index/app/worker/manifest SHA-256 fingerprints are unchanged.
Long histories passed: 44 source-cycle sessions/19 weeks, 36 coordinated workouts
across multiple months, get-up and club pathways, the full 42-exposure push-up
wave, 15 ground sessions and 13 unloaded/loaded hinge sessions. Coverage includes
partial work, technique/pain, missed months, equipment changes, skill gates,
short sessions, requalification, backup and offline persistence.

Final regression follow-up: the old club test expected an idle 00:00 display after
the first logged set. The repaired timer deliberately retains a continuous work
interval. Replaced that assertion with the actual invariant: one continuous work
entry, no inter-set rest, and a two-minute break only between movements. The full
34-exposure club history and get-up history pass. No engine rule was changed to
satisfy the test. Research checks pass all 30 existing rule quotes/hashes and the
720-record/23-system coverage inventory. Four preview-publisher tests pass.
Generated learning assets reproduce byte-identically. Final notes and public
countdown/pathway regression are a documentation/testing follow-up; the deployed
application source remains 7c6f2c0. No unfinished implementation remains locally.

## 2026-11-07 — UX review 2, notebook architecture checkpoint

Verified clean development branch at remote 062767c and inspected Train, timer,
engine replay, transaction/lock guards, draft validation and the existing tests.
Read the development/status/continuation/coverage/rules/review documents and full
warm-up overview #670. Reviewed existing movement-specific profiles rather than
replacing their methods. TRAIN-NOTEBOOK-DESIGN.md records boundaries.

Added pure notebook actuals/adjustment/outlook/correction functions. New draft
shape is opt-in and backward compatible; actual set count can differ from target.
Actual interval/rest edits deny credit. Corrections preserve previous versions,
rebuild queues and clear stale pending load choices. Nine new tests and every
existing Node suite passed. This is an architecture checkpoint: browser UI,
correction import validation and deployment remain unfinished; continue directly
with the commissioned interface and integration tests.

### UX review 2 — integrated Train/history checkpoint

Implemented ordered cycle inspection with navigable provisional lookahead and
recent records; only the next recommended workout can be started. Upcoming
prescriptions retain current evidence/loads, do not fabricate clean exposures or
future dates, and changes from the prior saved outlook are explained. Warm-up
and cooldown now contain explicit movements/doses, collapsible in preview/work.
Reviewed #670 pattern priming; exact routines remain labeled app defaults.

Train is a compact prefilled notebook with optional per-movement set editors,
load/reps/seconds, sides, timing/rest, notes, add/remove and bulk performed/skip.
Written, normal and adjusted plans are separate from actual results. Duration and
Pretty beat use the existing whole-work/recovery rules; Feeling great adds no
unearned work. Final confirmation records all non-skipped work, or only explicitly
performed work for a partial finish. The partial choice survives renders/reloads;
zero-work partials do not skip a programmed day. Timers never log work.

The repaired countdown is now compact/sticky throughout the workout. Instruction
opens in a dismissible overlay without changing draft or pacing. A rendered Pixel
5 touch flow passed 45→30/Pretty beat adaptation, prep, timer elapsed time and
scroll visibility, instruction return and one-save completion. A second complete
flow passed final-set modification, immutable targets, history correction,
replayed progression, reversible versions, backup/restore and offline reload.

Injected final-save and correction failures passed rollback/retry and duplicate
protection. Added/removed sets, partial draft reload, read-only second tab,
offline historical correction and malformed audit rejection passed. Existing
six DOM workflows, all three timer modes/frozen lifecycle, Learn, backup faults,
Web Locks/stale writes and old-worker draft upgrade passed with explicit optional
editor/partial-outcome actions. 44 source-cycle sessions and 36 coordinated
workouts passed. Remaining long history regressions and preview publication are
still running/pending; this checkpoint does not claim deployment or physical
Android testing. Node tests now include 12 notebook cases plus existing suites.
