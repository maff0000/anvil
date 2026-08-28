# ANVIL-WORKER-013B — External Baseline Reconciliation

## Inputs

- Local Email Builder HEAD: `14666da9470629031b442b94f1a978e79009ded7`
- Published GitHub `main`: `d30d8484827cff77a7ea281693deb1718d26ea19`
- Original local worktree: `/srv/codex/email-builder`

## Ancestry and provenance

The local repository has `origin/main` tracking GitHub `d30d848`; local
`main` is four commits ahead. The merge-base of both commits is exactly
`d30d848`. Local-only commits, in order, are:

| Commit | UTC | Subject |
|---|---|---|
| `c4cbc4d` | 2026-08-26 14:05 | Align email-builder with ACK v0.1.1 |
| `0360417` | 2026-08-27 07:05 | Make ACK worker preparation idempotent |
| `8e60fac` | 2026-08-27 10:18 | Document Git durability and worker watch feedback |
| `14666da` | 2026-08-27 11:09 | Synchronize ACK runaway-worker protection 951d3a3 |

There are no commits reachable from GitHub `main` that are absent locally.
The local-only commits change ACK control files, `AXIOM.md`, and `.gitignore`;
they do not add intended Email Builder product behavior.

## Committed tree comparison

`git diff d30d848 14666da -- app.py email_builder tests README.md PID.md
requirements.txt` is empty. The committed tree hashes are identical for:

- `app.py`: `fe13bc2...`
- `email_builder/`: `4e77b0c...`
- `tests/`: `9bf53ff...`
- `README.md`: `2fa2952...`
- `PID.md`: `503a51d...`
- `requirements.txt`: `fc35af2...`

Therefore:

- `BASELINE_RELATION: LOCAL_AHEAD`
- `MATERIAL_PRODUCT_DIFFERENCE: NO`
- local-only difference: ACK-era control/documentation machinery only.

## Authority decision

`DECISION: USE_PUBLISHED_GITHUB_BASELINE`

The published commit is the canonical, reproducible product baseline. The
local commits are newer chronologically but are unrelated ACK-era control
changes explicitly excluded from WORKER-013. Using GitHub `main` avoids
silently importing that machinery while preserving the complete committed
Email Builder product tree unchanged.

This is not a discard of product work: the relevant application, template,
test, README, PID, and dependency trees are byte-identical at both baselines.

## Preservation and reproducibility

The original worktree remained untouched at local HEAD `14666da` with 38
pre-existing dirty paths. No reset, clean, stash, stage, branch switch, or
application edit was performed there. A fresh HTTPS clone reproducibly checks
out published `d30d848` cleanly.

WORKER-013 resume baseline is therefore:

`d30d8484827cff77a7ea281693deb1718d26ea19`

in a new clean isolated clone, with feature branch `worker-013-template-
campaign` to be created before the PID commit. No Email Builder implementation
has begun.

`EXTERNAL_BASELINE_RECONCILIATION_VIABLE`
