# ANVIL-WORKER-002 — Native in-session Codex

Date: 2026-08-28 UTC  
Branch: `feature/worker-002-native-subagent`  
Accepted implementation commit: `9c6f13e`  
Substrate: first-party `multi_agent_v1` in-session collaboration tools

## Scope

This experiment tested only native in-session subagents. It did not launch
`axel`, `codex exec`, an app-server, or an external Codex process, and it did
not add ACK wrapping, bubblewrap, Redis machinery, or custom orchestration.

## Stage 0 — observed capabilities

The parent Axiom session used `multi_agent_v1__spawn_agent` with
`fork_context: false`, then `multi_agent_v1__wait_agent` and
`multi_agent_v1__close_agent`. A fresh child:

- ran in `/srv/codex/anvil` and could read the repository;
- had bash and could inspect/run project commands;
- could write repository files (confirmed by the Engineer task);
- could read Git and reported `.git` appeared writable, but made no Git writes;
- inherited no `ANVIL_*`, `REDIS_URL`, `REDIS_HOST`, `REDIS_PORT` variables;
- had no `redis-cli`, so Redis reachability was not established or modified;
- returned structured output directly to Axiom;
- was independently waitable and closable by Axiom.

The read-only probe did not execute tests. This was a probe constraint, not a
platform failure.

## Stage 1 — Engineer

Work item: `ANVIL-WORKER-002-METRICS-001`  
Allowed files: `anvil/metrics.py`, `tests/test_metrics.py`

The Engineer implemented a deterministic nearest-rank `percentile` helper
with finite-value and percentile-range validation, no input mutation, and
nine contract tests. Its returned evidence named the native in-session
substrate, the two changed files, and a passing focused test run:

`python3 -m unittest discover -s tests -p 'test_metrics.py'` — 9 passed.

## Stage 2 — Axiom reconciliation

Axiom independently inspected the actual untracked files, verified the exact
two-file scope, reviewed the implementation and tests, ran the focused suite,
and ran `./ops/validate`. The complete repository suite passed: 15 tests.
`git diff --check` passed. Axiom then committed and pushed the implementation;
the Engineer did not exercise Git authority.

## Stage 3 — fresh Auditor

A second fresh native in-session subagent was given the contract, resulting
source, diff commit, and test evidence, without Engineer reasoning. It made no
edits and returned:

`AUDIT_VERDICT: GREEN`  
Findings: none  
Confidence: high

It independently ran `python3 -m unittest discover -s tests -v` (15 passed),
edge-case checks, and `git diff --check`.

## Result

Engineer → independent PL reconciliation → fresh Auditor completed GREEN in
one implementation pass; no repair round was required. The native child
could perform bounded repository work and return evidence, while Axiom
retained scope, test, Git, and acceptance authority.

Classification: **NATIVE_SUBAGENT_VIABLE**

This is a one-task substrate proof, not evidence of unattended orchestration,
provider abstraction, Redis integration, or broad autonomous coding ability.

## Terminology correction

The prior external-process result is classified separately:

`external fresh Codex worker process = REJECTED_CURRENT_RUNTIME`

That result reflects managed in-process app-server runtime state being
read-only during external startup. It does not reject the native in-session
subagent mechanism tested here.
