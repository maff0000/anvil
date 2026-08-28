# ANVIL-WORKER-004 — Native multi-Engineer decomposition and integration

Date: 2026-08-28 UTC  
Branch: `feature/worker-004-native-multi-engineer`  
Final commit: `a9ab7a9`  
Substrate: first-party `multi_agent_v1` in-session Codex subagents

## Overall contract

Build a useful, bounded ANVIL capability for deterministic benchmark-result
handling: normalize one raw attempt into a stable outcome value, then render a
sequence of outcomes as deterministic Markdown. The feature must be
standard-library-only, deterministic, non-mutating, strictly validated, and
must support every finite non-negative integer or float duration accepted by
the normalizer, including arbitrary-size integers.

No production runtime, model routing, configuration, Redis, broker, scheduler,
lease, sandbox, provider abstraction, or unattended machinery was changed.

## Decomposition

The decomposition was committed before either worker was spawned in
`5da8a74`.

Engineer A (`ANVIL-WORKER-004-OUTCOME-001`) owned only
`anvil/outcomes.py` and `tests/test_outcomes.py`: the frozen `AttemptOutcome`
interface and `normalize_attempt` raw-record normalizer.

Engineer B (`ANVIL-WORKER-004-REPORT-001`) owned only
`anvil/outcome_report.py` and `tests/test_outcome_report.py`: the renderer
consuming only A's public `AttemptOutcome` interface.

Axiom owned only the predeclared integration seam,
`tests/test_outcome_integration.py`, plus Git and evidence documentation.

Workers were spawned concurrently by direct Axiom calls and waited on directly;
no scheduling machinery was added.

## Engineer A

Engineer A returned the two authorized files and reported six focused tests
passing. Axiom independently inspected the files and later verified the
normalizer as part of the full integration suite. Its implementation provided
strict field validation, status partitioning, exact timeout markers, frozen
outcomes, input immutability, and large-number preservation.

Engineer A's report incorrectly claimed that no native in-session tool was
exposed. That claim is contradicted by the actual successful
`multi_agent_v1__spawn_agent`/wait execution and prior WORKER-002 evidence. It
did not affect the code result and is recorded as a worker-report quality
discrepancy, not accepted as project fact.

## Engineer B

Engineer B returned the two authorized renderer files and reported its focused
tests passing. It implemented deterministic Markdown summary counts, totals,
fixed formatting, ordered rows, and non-mutating behavior. Axiom verified that
it consumed the stable public interface rather than raw mappings.

## Axiom reconciliation and integration

Axiom independently verified exact non-overlapping scope and ran the focused
worker suites, full tests, `./ops/validate`, and `git diff --check`. Axiom added
only the predeclared end-to-end test that passes raw records through A's
normalizer and B's renderer. This was administrative integration/test wiring,
not substantive production implementation.

The first integrated candidate was committed as `1a2cc62` and pushed.

## Auditor and repairs

### Auditor 1 — RED

The fresh Auditor found a valid interface defect: B crashed when rendering
the valid `wall_seconds=10**400` accepted by A. Axiom reproduced and validated
the finding.

### Repair round 1

A fresh Engineer B repair changed only B's module and tests, using Decimal
formatting and adding a regression test. Axiom reconciled the result and
committed `481cdb4`.

### Auditor 2 — RED

A fresh Auditor found a second valid precision defect: Decimal's default
context lost the fractional result for mixed arbitrary-size durations such as
`[10**400 + 1, 0]`. It also found trailing whitespace in the decomposition
document. Axiom validated the numeric finding; the whitespace was an
administrative evidence correction.

### Repair round 2

A fresh Engineer B repair replaced context-limited Decimal aggregation with
exact Fraction arithmetic and deterministic six-decimal round-half-even
formatting, adding mixed-extreme and even-median tests. It changed only B's
module and tests. Axiom removed the evidence whitespace, then independently
reconciled the result and committed `a9ab7a9`.

### Final Auditor — GREEN

A third fresh Auditor independently verified the final source and diff:

`AUDIT_VERDICT: GREEN` — high confidence

It verified arbitrary-size integers, mixed huge/small values, even medians,
large finite floats, ordering, exact interface/keys, immutability, scope, and
the raw-record-to-renderer integration. No findings or repairs remain.

## Final evidence

- Engineer invocations: 4 total (A, B, and two fresh B repair Engineers)
- Auditor invocations: 3 total
- Repair rounds: 2, the configured maximum
- Worker scope violations: none
- Hidden coupling: one real numeric interface mismatch, found by integration
  audit and repaired without PL coding takeover
- Full pytest: 44 passed, 54 subtests
- Full unittest/`./ops/validate`: 35 passed
- `git diff --check`: passed
- Production impact: none
- Human intervention: none
- Final classification: **NATIVE_MULTI_ENGINEER_VIABLE**

The native workers successfully decomposed, implemented, integrated, and
repaired a useful feature. The result is conservative: one bounded feature
does not prove broad multi-worker autonomy.

Exact worker lifecycle timestamps and token telemetry were unavailable from the
collaboration API and are not fabricated. The API did expose successful spawn,
wait, completion, and closure operations. Raw operational details remain in
the session/tool evidence; this committed summary contains the reproducible
technical facts needed for scrutiny.

## Governance lessons

Useful controls were explicit parent/subcontracts, non-overlapping file scope,
a predeclared stable interface, Axiom-owned integration and Git, independent
reconciliation, fresh Auditor separation, concrete finding adjudication,
bounded repair rounds, deterministic tests, and committed evidence.

Unnecessary controls were a scheduler, queue, broker, Redis control plane,
leases/fencing, nested sandboxing, worker-owned Git, provider abstraction, and
a workflow state machine. Direct native spawning and waiting were sufficient.

The decomposition exposed one genuine governance need: Axiom must reconcile
interfaces across independently correct-looking components and ensure that
integration edge cases are tested. That need is satisfied by explicit
integration ownership and independent audit; no new machinery is justified.
