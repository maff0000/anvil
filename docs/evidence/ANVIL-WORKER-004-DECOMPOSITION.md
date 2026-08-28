# ANVIL-WORKER-004 decomposition

Parent work item: `ANVIL-WORKER-004-NATIVE-MULTI-ENGINEER`  
Feature: deterministic benchmark-result outcome normalization and rendering

## Engineer A — outcome normalization

- Work item: `ANVIL-WORKER-004-OUTCOME-001`
- Allowed files: `anvil/outcomes.py`, `tests/test_outcomes.py`
- Responsibility: validate one raw attempt record and produce a stable
  `AttemptOutcome` value object.
- Inputs: one mapping with `syntactic_validity`, `semantic_pass`,
  `wall_seconds`, `output_tokens`, optional `finish_reason`, and optional
  `error`.
- Outputs: `AttemptOutcome` with the normalized booleans, numeric telemetry,
  and a `status` of `accepted`, `syntax_failure`, or `semantic_failure`.
- Acceptance: strict validation, timeout/truncation flagging, no mutation,
  deterministic standard-library behavior, and focused tests.

## Engineer B — outcome rendering

- Work item: `ANVIL-WORKER-004-REPORT-001`
- Allowed files: `anvil/outcome_report.py`, `tests/test_outcome_report.py`
- Responsibility: render a deterministic compact Markdown report from a
  sequence of `AttemptOutcome` values.
- Inputs: the stable `AttemptOutcome` interface above; no raw-record parsing.
- Outputs: Markdown containing fixed summary counts and telemetry totals in
  input order.
- Acceptance: deterministic output, empty-sequence rejection, no mutation,
  and focused tests. No imports from or edits to Engineer A's tests.

## Integration contract owned by Axiom

Axiom will add only `tests/test_outcome_integration.py` after both workers
finish. It will construct raw records, normalize them through Engineer A's
public function, pass the resulting values to Engineer B's public renderer,
and assert the end-to-end report. Axiom owns this integration seam and all
Git operations. No worker may edit the other worker's files or `.git`.
