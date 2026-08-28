# ANVIL-WORKER-013A — External Git Authority Re-proof

## Original failure and root cause

WORKER-013 could not begin in `/srv/codex/email-builder`: creating a branch
failed with `.../.git/refs/heads/...lock: Read-only file system`. Read-only
mount inspection confirmed that Email Builder's `.git` is mounted from the
host filesystem with `ro` options. The managed shell has ordinary `git`, `gh`,
and `axel`, but no separate host Git/MCP authority path was exposed.

## Mechanism selected

`OPERATING_MODEL: CLEAN_ISOLATED_CLONE`

Axiom uses a standard temporary clean clone under `/tmp`, sets its remote to
the published Email Builder GitHub URL, and performs explicit Git operations
there. This is bounded by the explicit clone path and repository remote; it
does not require making the source `.git` writable and does not add a service,
broker, registry, lease, or workspace framework.

## Proof

The clone was made from the current local Email Builder repository at
`14666da`, which gives a clean committed snapshot without copying the dirty
untracked ACK-era files. In the clone Axiom:

1. created `proof/worker-013a-git`;
2. created only `.anvil-worker-013a-proof`;
3. staged that exact path, never `git add .`;
4. committed it as `459a6c5` after setting identity locally in the disposable
   clone only;
5. inspected clean status, history, and `git diff --check`;
6. pushed successfully to `https://github.com/maff0000/email-builder.git`;
7. deleted the disposable remote proof branch after the push was proven.

The initial push to the local clone source remote failed with Git's unpacker
error because that source `.git` is read-only. Switching the disposable clone
remote to GitHub succeeded. This precisely identifies the usable push path.

## Real repository boundary and dirty-worktree protection

Read-only checks against `/srv/codex/email-builder` confirmed:

- HEAD remains `14666da9470629031b442b94f1a978e79009ded7`;
- 38 pre-existing modified/untracked paths remain present;
- no Email Builder application file was changed, staged, reset, stashed, or
  cleaned by WORKER-013A.

The isolated clone is therefore the safe WORKER-013 operating model. Axiom
will copy only explicitly selected product files into a clean clone/worktree
derived from the committed baseline, inspect and stage explicit paths, then
push the feature branch to GitHub. The original dirty worktree remains
untouched. Standard Git worktree creation directly from the original is not
available while its `.git` mount is read-only.

## Authority boundary

Axiom/PL retains Git authority in the isolated clone. Native Engineers and
Auditors receive no Git responsibility and will not be given the clone's Git
credentials or Git lifecycle instructions. They work only within the bounded
project task; Axiom reconciles files and owns branch, staging, commit, push,
and PR operations.

## Result

`EXTERNAL_GIT_AUTHORITY_VIABLE`

Branch creation, explicit staging, commit, history/status inspection, and
GitHub push are proven. PR creation is available through `gh` from the same
published remote; it was not created for the disposable proof branch. No new
ANVIL application code or framework mechanism was required.

WORKER-013 may resume from completed repository discovery by using
`CLEAN_ISOLATED_CLONE`, creating its PID before implementation in that clean
delivery clone, while leaving `/srv/codex/email-builder` unchanged.
