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
