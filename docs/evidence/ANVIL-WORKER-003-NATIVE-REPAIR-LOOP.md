# ANVIL-WORKER-003 — Native repair loop

Date: 2026-08-28 UTC  
Branch: `feature/worker-003-native-repair-loop`  
Final implementation commit: `a8b5a73`  
Substrate: first-party `multi_agent_v1` in-session Codex subagents

## Experiment

This experiment tested one bounded Engineer → Axiom reconciliation → fresh
Auditor → adjudicated repair → reconciliation → fresh Auditor sequence. No
external Codex process, ACK/PBG machinery, Redis, broker, lease, or unattended
loop was introduced.

## Task contract

`ANVIL-WORKER-003-EVIDENCE-SUMMARY-001` added
`anvil.evidence_summary.summarize_attempts`. The function validates benchmark
attempt records, partitions accepted/syntax/semantic outcomes, counts exact
timeout-or-truncation markers once, and returns deterministic token/timing
summary statistics. It must reject malformed records, preserve input data,
use standard-library code only, and return the specified eight keys.

Allowed files were exactly:

- `anvil/evidence_summary.py`
- `tests/test_evidence_summary.py`

## Engineer 1

Fresh native in-session Engineer, `fork_context: false`, reported both file
changes and 12 focused tests passing. The actual candidate added the utility
and authoritative coverage. The Engineer had filesystem and test access and
did not use Git authority.

## Axiom reconciliation 1

Axiom independently inspected the actual files and diff, verified the exact
two-file scope, ran focused and full tests, and ran `git diff --check`.

At candidate commit `0283493`:

- full ANVIL suite: 27 tests passed;
- scope: exactly the two authorized files;
- diff check: passed;
- no unrelated runtime/config changes.

Axiom committed and pushed the candidate. The Engineer did not commit or
push.

## Auditor 1

Fresh native in-session Auditor, without Engineer reasoning, returned `RED`.
The finding was valid and reproducible: `isfinite(10**400)` raised
`OverflowError`, despite that value being a valid finite non-negative integer;
two valid `1e308` durations also produced an infinite mean/median aggregate.
The supplied tests did not cover those boundaries. Partitioning, timeout
de-duplication, exact keys, immutability, scope, and standard-library use were
found correct.

Axiom adjudicated the finding as valid against the written contract.

## Repair

One fresh repair Engineer received only the contract and the validated
finding. It changed the same two authorized files, used `Decimal`
intermediates to avoid range/aggregate overflow, and added boundary tests.
It reported 29 tests passing. No PL coding takeover occurred.

Repair commit: `a8b5a73` (`Repair large-duration evidence aggregation`).

## Axiom reconciliation 2

Axiom independently inspected the repair, verified scope, ran the full suite,
ran `./ops/validate`, and checked `git diff --check`.

## Auditor 2

Fresh native in-session Auditor, without prior Engineer reasoning, returned:

`AUDIT_VERDICT: GREEN`

It independently verified arbitrary-large-integer handling, large finite
float handling, mixed values, immutability, exact keys, partitioning, timeout
de-duplication, and invalid inputs. Full suite result was 29 tests passed.
No findings or required repairs remained; confidence was high.

## Final result

- Engineer invocations: 2 (initial implementation plus one repair)
- Auditor invocations: 2
- Repair rounds: 1
- Genuine RED finding: yes
- Axiom adjudication: valid, evidence-confirmed
- Final Auditor: GREEN
- Final tests: 29 passed; `./ops/validate` passed; `git diff --check` passed
- Human intervention: none
- Final classification: **NATIVE_REPAIR_LOOP_VIABLE**

The native mechanism demonstrated bounded recovery from an independently
detected, contract-valid edge-case defect. This is stronger evidence than a
single naturally GREEN implementation, but it is still one task sequence and
does not prove unattended orchestration or broad autonomous repository work.

## Lifecycle evidence and limitations

The collaboration API returned child IDs and completion results but did not
expose per-call UTC timestamps or token/usage telemetry. Therefore exact
spawn/completion times and usage are recorded as unavailable rather than
invented. Parent orchestration observed successful spawn, wait, completion,
and closure of the probe/child sessions. Git commit timestamps provide the
durable implementation checkpoints.

Redis was not used: the current native worker environment did not naturally
provide Redis tooling/configuration, and this experiment did not modify the
worker mechanism to force it.

## Governance lessons

Useful controls were the explicit file scope and contract, fresh Engineer and
Auditor separation, independent PL reconciliation, Axiom-owned Git, concrete
Auditor evidence, bounded repair count, deterministic tests, and durable
committed evidence.

Unnecessary controls were Redis state, leases/fencing, worker-owned Git,
custom brokers, nested sandboxes, provider abstraction, and an autonomous
workflow engine. None solved an observed WORKER-003 problem. The repair loop
remained a small sequence of native invocations governed at the authority
transitions.
