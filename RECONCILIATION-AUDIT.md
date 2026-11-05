# Strength Lab reconciliation audit

Audit date: 2026-11-05. Baseline: `4cb58d8a4d30796246a83db752b8e420c8bc05c2`.
Development branch: `development/reconciliation`.

## Evidence and limits

The existing checkout contains 28 commits. GitHub read access confirms that remote
main and HEAD match the baseline. History is preserved; no reset, replacement,
merge into main, release, or push was performed.

The user reports publication. This conversation is still bound to the same
onboarding instance; runtime status reports the original source version. A fresh
task cannot be created with the available tools, so fresh-task restoration is
**unverified**. Current-instance Node/Python availability and the existing smoke
test are verified.

No ZIP files or development handoff are attached in the accessible conversation.
Searches of /workspace (including library-files, shared and scratch) found none.
A broader /tmp search encountered inaccessible system-owned directories; those
were not inspected. No upload IDs were supplied to the download tool. Therefore
comparison against either ZIP and the handoff is **blocked**, and no implementation
can honestly be ranked against those missing alternatives. Attach both ZIPs and
the handoff to resume that part of the audit.

## Repository findings

| Area | Current implementation | Decision |
| --- | --- | --- |
| Architecture | Static HTML/CSS/JS, browser local storage, service worker; no package manifest, backend or build | Preserve dependency-free runtime |
| UI | V32 minimal design and six tabs; previous commit comparison shows additive visual/navigation changes and source index | Preserve current UI pending handoff comparison |
| Training | V31 ABC rolling sequence and clean initial state; documented smoke test passes | Preserve engine and storage key pending behavioral comparison |
| Data | `strengthlab-data-v31`, JSON/CSV backup; no automatic cloud backup | Preserve existing data; do not claim cloud sync |
| Offline | HTML requests app/CSS/manifest with `?v=32`, but install precaches unversioned URLs | Confirmed first-visit offline defect; fix exact shell precache URLs and invalidate old cache |
| Tests | Node VM smoke test covers sequence, preparation and estimator; no checked-in browser regression | Add real Chromium coverage for first-visit offline startup and navigation |
| Documentation | README begins with V18 deployment text; VERSION and design notes identify V32 | Treat older README claims cautiously; defer broad rewrite until handoff is available |

## Integration boundary

Repository-only inspection is complete for the first offline repair. Full
reconciliation remains pending the two ZIPs and handoff. Proceed with the
independently reproduced offline defect; do not import guessed implementations
or alter training progression without evidence. Keep audit and development status
updated with executed checks and recoverable local commits.
