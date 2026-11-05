# Strength Lab reconciliation audit

Updated 2026-11-05. Branch: `development/reconciliation`.
Baseline: `4cb58d8a4d30796246a83db752b8e420c8bc05c2` (28 original commits).
Prior development checkpoints: `ccbb31f` and `bbf8085` remain ancestors.

## Input access and integrity — verified

Both attachments were downloaded into `/workspace/attachments`, opened with
Python's ZIP reader, integrity-tested, checked for path traversal, and extracted
outside the Git checkout into `/workspace/reconciliation-inputs`.

| Input | Bytes | SHA-256 | Contents |
| --- | ---: | --- | --- |
| Transcripts.zip | 2,174,926 | `b4940dcec1a9dc7eb5a64ec7a6bd92b8d0d428cfaf8d8dc02f94d2edb45edf9a` | 720 text transcripts plus directory entry |
| strength-lab-work-handoff-source.zip | 1,810,412 | `2b506d7a623d9cad44ef13547770e4bc4f856c89a1fae7f95851271d53c147aa` | 48 files plus directory entry |

The earlier missing-input findings are resolved. Instructions inside the handoff
(e.g. replacing the repository root or deploying a release candidate) were treated
as historical reference, not authorization. The current user request governs.
No merge into main, release package, history rewrite, or push was performed.
GitHub read access was rechecked; remote main remains at the baseline.

## Published environment restoration — not independently verified

Current-instance Node, Python, Playwright, Chromium, GitHub access, local HTTP,
and browser storage work. Runtime status still reports the same onboarding
instance and original source version. Available tools cannot create a fresh cloud
task, so this is not evidence of fresh-task snapshot restoration. Fresh browser
contexts used below verify application first-run/offline behavior only.

## File and implementation reconciliation

`research/handoff-file-comparison.json` records every handoff file's SHA-256 and
its baseline counterpart. All 48 files were inventoried: 39 added, nine changed,
none identical. Source history is preserved rather than replaced.

| Area | Repository baseline | Handoff | Integration decision |
| --- | --- | --- | --- |
| App/UI | V32 six tabs, V31 data model, monolithic code | Four tabs, active-set focus, per-set logging, persistent draft, rest controls | Integrate the newer execution interface; retain the old interface under `legacy/` |
| Training | Heuristics embedded in UI | Pure engine with independent movement ranges, duration fitting and deferred work | Integrate, then repair the defects below; exact progression numbers remain app defaults |
| Data | `strengthlab-data-v31` | Separate V33 workout/draft keys | Preserve both, expose old log/backup link; never reinterpret incompatible old records as verified new-engine exposures |
| Research | 720 title records with YouTube IDs | 720 title records, 24 full-text shards, topic map | Integrate verified full text; retain original inventory for legacy Atlas |
| Offline | First-visit query-string defect already repaired on branch | Broad precache but cache writes not tied to fetch lifetime | Preserve first-visit guarantees, await cache writes through event.waitUntil; cache new and legacy paths |
| Tests | VM sequence smoke test | Engine/completion tests and several browser scripts | Keep legacy smoke; adopt useful tests, repair stale selectors/no-op assertion, add real HTTP/storage/offline tests |
| Research notes | No research workbench | Notes reference many additional prototypes | Inventory-only claims: those modules are absent, so do not claim they were integrated |

Absent claimed files include `build_research.py`, `research-audit.json`,
`build_concordance.py`, `research-concordance.json`, `snatch-cycle.js`,
`program-composer.js`, `movement-cycles.js`, associated tests and review packs.
The handoff README's blanket claim that browser testing was blocked conflicts
with included later DOM tests; executed checks below replace those stale claims.
The provided `browser_smoke.py` uses file navigation and obsolete Learn selectors;
it was superseded by the real HTTP test instead of counted as passed.

## Transcript-to-index comparison — complete mechanical audit

`python3 scripts/audit-transcripts.py /path/to/Transcripts` compared every original
by its VIDEO URL against every full-text record, stripping the metadata preamble
and normalizing whitespace only. `research/transcript-audit.json` records source
filenames, URLs, normalized-text hashes, word counts, and per-record results.

- 720 originals, 720 unique indexed IDs, 720 full-text records in 24 shards.
- 955,522 whitespace-delimited transcript words.
- Zero missing URLs, text mismatches, title/index mismatches or word-count mismatches.
- The baseline title index covers the same 720 video identities and word counts.
- Handoff IDs are numeric positions; baseline IDs are YouTube IDs. They are not interchangeable.
- 158 topic labels differ between baseline and handoff. Labels are heuristic title
  groupings, not manually verified research conclusions.

Full text of sources #666 (volume cycles), #670 (warmup design), and #259
(adjusting stalled progress) was read in this reconciliation pass. These use the
handoff's zero-based IDs, now also shown consistently in the reader. They support
fixed-intensity volume practice, pattern-specific preparation and adapting a
stalled plan. They do not establish the app's precise start/end sets, rest periods,
two-exposure safeguard, readiness fraction or absence threshold. Source #259
shows alternative rep/set strategies; a general-purpose automatic implementation
still requires movement-specific analysis. Mechanical fidelity is not a claim of
careful interpretation of all lessons or scientific/medical validation.

## Repairs and unfinished training intelligence advanced

1. Pain holds persist across load changes and low-readiness selection. Held
   movements are omitted from training until explicit user review. Review is
   associated with stable record identities so deleting earlier history cannot
   clear a later pain event. Return after review starts with reduced work.
2. Re-entry is calculated per movement, so frequent unrelated training cannot
   conceal a long absence from a particular movement. Training can be paused
   and resumed explicitly without discarding progression history.
3. `performed` is separate from advancement eligibility. Clean reduced work
   finishes a movement without earning advancement or perpetually deferring it.
   A clean rebuild can exit the repeated-difficulty state.
4. Bilateral prescriptions require explicit confirmation of both sides/directions;
   invalid numbers, fractional reps, mixed loads and partial work cannot advance.
5. Each movement retains its own provisional volume range. The unsupported
   automatic generic density progression was removed: volume endpoints require
   a user-controlled milestone/load decision. `policyFor` exposes provenance.
6. Empty equipment lists defer affected movements. Complete prescriptions are
   fitted within whole-minute 15–120-minute session budgets without truncating sets.
7. Warmup uses the actual scheduled movements (including deferred carryovers),
   and warmup/cooldown instructions match the selected duration. A source lesson
   can be opened directly. The main clock uses the actual selected main budget.
8. Full-text search no longer discards body-only matches via a second title filter.
9. Backup validation rejects malformed profiles before replacement. Failed workout
   persistence retains the draft and restores in-memory session state.
10. Legacy app, Atlas inventory, styles, data key and export tools remain accessible.
    Existing workouts are not silently migrated to incompatible prescriptions.

## Executed validation

- Original legacy VM smoke test: passed against preserved `legacy/app.js`.
- Handoff engine assertions and three completion tests: passed.
- Thirteen new recovery/progression/equipment tests: passed.
- Three backup validation/roundtrip tests: passed.
- JS syntax checks and Git whitespace checks: passed.
- Six reconciled Chromium DOM suites: focus, duration, timer controls/modes,
  timer lifecycle and learning navigation passed. These use simulated storage.
- Real HTTP Chromium suite at `/` and `/strength-lab/`: first-visit offline
  reload, body-only search, full transcript reader, navigation, workout saving,
  persistent drafts/rest pause, bilateral logging, pain review and legacy storage.
  Actual browser storage is used, with no JavaScript page errors.

A regression test exposed that rounding 70% of three sets upward left re-entry
unchanged; rounding was corrected to ensure reduced work and the test now passes.
Existing timer selector and duration test no-op were corrected rather than
reported as useful passing assertions.

## Remaining development boundaries

The source/repository mechanical reconciliation is complete. A complete lifelong
source-grounded training system is not. Still needed: close reading across
movement-specific club/grind progression lessons, prerequisites and skill gates,
program-overlap/fatigue composition beyond the current ABC default, explicit
source-specific progression options, and broader installed-PWA/Android testing.
The current recovery thresholds and program rotation remain app defaults.
Fresh-task environment restoration remains unverified. No release is authorized.

## Training intelligence continuation — 2026-11-05

The historical remaining-work section above is superseded for the selected
programming systems by TRAINING-RULES.md and current DEVELOPMENT-STATUS.md.
Source-scoped profiles now distinguish #411 snatch volume, #410 snatch density,
#366/#120 double-grind examples, #228/#403 heavy/light principles, and #3 club
timed practice. Eleven quote anchors and hashes are checked against the already
verified source corpus. #259 supports stall alternatives; its failure classification
and rounding remain explicit app decisions. #561's individual recovery account
is not presented as an automated rehabilitation prescription.

Program-specific deferrals and configurable overlap/calendar/load controls are
integrated into the application. Existing ABC history, V33 data keys and V31/V32
access are preserved. Source cycles are opt-in, never automatically assigned as
new advanced skills. Recovery-adapted numerical prescriptions lose the exact-source
parameter claim while retaining their principle citations. Configurable defaults
do not acquire fabricated source support.

Validation now includes complete multiweek engine histories and actual HTTP
application histories (44 successful snatch exposures plus adverse/recovery cases;
six ABC workouts plus double/club controls). Cadence and skill input remain
self-reported. A real baseline-to-current service-worker upgrade passed while
preserving active data/draft bytes, then continuing offline. This supersedes the
previously outstanding browser worker-upgrade check; physical Android and fresh
cloud-task restoration remain unverified.

## Persistent recovery and curriculum coverage continuation — 2026-11-05

The user explicitly authorized pushing the development branch. It is now stored
on origin, with no force-push or change to main. The earlier local-only statements
refer to previous checkpoints. A fresh Git checkout recovered the prior completed
branch at `fe744c4`; a second fresh checkout recovered curriculum checkpoint
`2817a3f`, passed Git object checks, 22 programming tests, 10 curriculum tests,
16 source quote/hash checks and the 720-record coverage check.

All 720 full texts were screened into the 23-system coverage matrix. Its keyword
evidence is candidate discovery; source-grounded implementation claims use the
separate close-read rule manifest. The matrix distinguishes implemented scopes
from partial and missing systems and identifies the next curriculum priorities.

Implemented selected get-up alternating time goals (#423/#658) and continuous
single-arm club foundation volume/rest (#578/#581), with prior-foundation teaching
from #543 and shared prerequisite definitions. Actual application histories cover
56 new-system sessions, including failures/recovery, in addition to prior suites.
The complete get-up/club advanced curricula remain incomplete. Android packaging
was intentionally not started. Fresh Git recovery is not a fresh Codex snapshot
restoration test; the latter is still unavailable with current tools.
