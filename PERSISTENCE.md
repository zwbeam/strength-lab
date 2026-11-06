# Development branch recovery

Repository: `https://github.com/zwbeam/strength-lab.git`.
Branch: `development/reconciliation`. Main is not the development target.

On 2026-11-05 the previously local branch was pushed with ordinary Git (no force).
Remote main remained `4cb58d8a4d30796246a83db752b8e420c8bc05c2`.
A separate fresh checkout at `/tmp/strength-lab-recovery.9bgRzs` recovered
`fe744c40a6928afef6799de1602e14b5592851d2`, passed `git fsck --full`, and
passed all 22 programming tests. The complete earlier history is reachable from
that remote branch. This verifies GitHub persistence independently of the current
workspace's filesystem lifetime. Later verified work is pushed to the same branch.

A genuinely fresh Codex task cannot be launched by the tools available in this
conversation. Cloud snapshot restoration and future-task authentication therefore
remain unverified. A fresh Git checkout is a separate, successfully tested claim.

## Continue from another task

1. Select the existing `zwbeam/strength-lab` repository in Codex.
2. Select branch `development/reconciliation` rather than main.
3. Ask Codex to verify its local HEAD against the remote branch, read
   DEVELOPMENT-STATUS.md and DEVELOPMENT-LOG.md, and continue without resetting
   or rewriting history.

No token or interactive login was required here: the existing platform Git
proxy supplied access. Do not put credentials into chat or repository files.

## Curriculum checkpoint recovery

The code at `2817a3fa76c360deb49efa7128f04eddaed3c7a5` was pushed and recovered
into `/tmp/strength-lab-curriculum-recovery.lR4KCo`. Its objects verified with
`git fsck --full`; 22 programming tests, 10 curriculum tests, 16 provenance
quote/hash checks and the 720-source coverage/registry check passed there.
Later verified fixes and documentation are pushed normally to the same branch;
compare remote `refs/heads/development/reconciliation` with local HEAD before
continuing. Main must remain unchanged.

## Interrupted-task recovery verified — 2026-11-06

GitHub contained `b07a0e7`, including both movement commits after the user's last
confirmed `6269cab`. The unfinished backup edits were local only; the absent
browser test was recreated and tested. Completed recovery work was normally
pushed at `6c3df46`, expanded backup tests at `c266c97`, ground foundations at
`da8af31`, and recovery/import integrity at `d99a153`.

An independent clone of the private development branch into
`/tmp/strength-lab-resume-recovery-lv0tn0l2` recovered exactly
`d99a15364beeb62ae04c753c4cb790e68392d827`. `git fsck --full`, all root Node
suites (82 named tests plus engine assertions), 29 provenance anchors, all-720
coverage/registry checks, and actual Chromium backup/ground history suites passed
there. Recovery did not copy files from the working repository. Main remained
`4cb58d8a4d30796246a83db752b8e420c8bc05c2`.

This proves remote source recovery, including the recreated failure tests. The
available tools cannot launch a genuinely fresh Codex task. Cloud snapshot
restoration, fresh-task credentials, physical Android behavior and hardware
storage durability remain distinct unverified claims. Do not rely on this local
checkout or its temporary independent clone surviving a task boundary.

## Exclusive write ownership

Updated V33 clients hold the browser Web Lock `strengthlab-v33-writer` for their
page lifetime. Only that owner may recover a journal or write state/drafts.
Other tabs can view current saved data, read research and export backups; editing
and import are blocked. Close the editing tab and reload another tab to resume
from the latest saved state. Locks are released by the browser when a page closes
or crashes, rather than by an expiring localStorage lease that could split writers.

Startup recovery occurs only after ownership. A reader encountering a journal
reads the pre-transaction snapshot and does not roll back another tab's write.
Before every save, the owner compares raw history/draft values with its last known
saved snapshot. Unexpected storage events/values freeze writes and retain local
work for export, protecting against stale overwrite by this updated client.
Reload after closing other tabs to reconcile from saved data. Generic settings
and history edits also use the journaled pair transaction; failed saves no longer
leave apparently successful in-memory settings.

Web Locks require a supported browser on HTTPS or localhost. Without support the
app remains read/export-only rather than using a race-prone fallback. Physical
Android/Capacitor WebView support still needs device testing. Older already-open
application versions cannot be made to honor the new lock; close those tabs when
upgrading. Unexpected old-client changes are detected, but old code itself cannot
be prevented from writing. These guarantees do not cover physical storage loss,
user-cleared browser data or arbitrary external storage modification.

`tests/multi-tab.py` verifies real same-origin ownership, read-only import/save
rejection, live set/timer snapshots, reader behavior during a transaction,
close/reload draft handoff, duplicate-save protection, external and synchronous
stale-write detection, unsaved-draft export, offline reload and unsupported-lock
read-only mode. The existing fault-injection and worker-upgrade suites pass.

## Executor recovery and remote continuity — 2026-11-06

The previously failed executor became usable again. Verified actual shell, Git,
Node and Chromium operations rather than relying only on the status service.
The same workspace contained three interrupted files. Remote HEAD was `a68b180`,
with `b05b82c` and `ea80b41` confirmed ancestors and no newer remote work.
Reviewed and independently checkpointed chronology `8e35d01`, corrected browser
histories `1280712`, and cadence feedback `7e4a049`.

A separate GitHub clone at `/tmp/strength-lab-recovered-checkout-s910hab1`
recovered exactly `7e4a04914c0306830bf27f433183a421d5f7daf8`, verified objects with
`git fsck --full`, and passed every root Node suite (98 named tests plus engine
assertions), 30 source quotations/hashes, all-720-source registry coverage, the
actual cadence workflow and real multi-tab reliability suite. No working-tree
files were copied into it. Later documentation commits may follow.

This verifies GitHub recovery and the restored executor, not a new empty Codex
task/snapshot or guaranteed persistence of future local edits. Keep pushing tested
increments. A cloud status response can say running even when actual executor
commands fail; shell/browser checks remain necessary. Main was not changed.
