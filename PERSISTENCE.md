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
