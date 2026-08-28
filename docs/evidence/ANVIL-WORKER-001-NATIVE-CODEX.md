# ANVIL-WORKER-001-NATIVE-CODEX

## Result

Classification: `NATIVE_WORKER_REJECTED`

The native Engineer could not start under the managed Codex runtime. No
Engineer code, tests, Git operation, or Auditor invocation occurred.

## Attempt

- UTC date: 2026-08-28
- Worker: fresh native Codex Engineer
- Mechanism: `/usr/local/bin/axel -C /srv/codex/anvil exec --sandbox workspace-write --ephemeral -`
- Project path: `/srv/codex/anvil`
- Intended work item: `ANVIL-WORKER-001-NATIVE-CODEX`
- Intended scope: `anvil/metrics.py`, `tests/test_metrics.py`
- Intended runtime: native Codex with the managed workspace-write sandbox
- Git authority supplied: none
- Command result: exit 1 before worker initialization
- Exact error: `failed to initialize in-process app-server client: Read-only file system`

## Boundary observations

- The launcher was invoked directly; ANVIL did not wrap the worker.
- No child Codex process remained after failure.
- The repository remained unchanged and no `.git` operation was attempted.
- Filesystem permissions could not be exercised by the Engineer because the
  in-process app-server failed before task execution.
- Redis was not tested because no worker process started; no Redis schema or
  worker integration was added.
- No model/provider usage or token telemetry was available.
- No Auditor was spawned because there was no Engineer delivery candidate to
  reconcile.

## PL outcome

Axiom retained Git authority and did not fabricate an Engineer result. No
repair iteration was assigned. Existing ANVIL production/model services were
not changed. The failure is a platform substrate limitation, not evidence
about coding quality.

Validation after the failed spawn: the existing ANVIL test suite remained
GREEN and `git diff --check` was clean.

## Next step

Native Codex spawning cannot become the baseline worker substrate until the
managed app-server has safe writable runtime state. Resolving that boundary
requires platform authority; ANVIL will not bypass or weaken managed controls.
