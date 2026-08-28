# ANVIL-WORKER-005 work contract

Parent work item: `ANVIL-WORKER-005-NATIVE-ENGINEER-LOCAL-GPU`

## Native Engineer

- Owns the surrounding integration in `anvil/outcome_report.py` and its
  focused tests in `tests/test_outcome_report.py`.
- May add the bounded GPU-produced helper to the existing renderer and add
  the corresponding success-rate line and tests.
- May use existing ANVIL inference code only for the declared GPU call.
- May not change model serving, production routing, Git, or unrelated files.

## Local GPU subtask

Generate only this pure Python function:

`format_success_rate(numerator: int, denominator: int) -> str`

Contract:

- `denominator` must be a positive `int`; `bool` is invalid.
- `numerator` must be an `int` in the inclusive range `[0, denominator]`; `bool`
  is invalid.
- Raise `ValueError` for invalid values.
- Return the exact percentage as a string with one decimal place and a trailing
  `%`, using deterministic round-half-even behavior. Examples: `0/3` →
  `0.0%`, `1/8` → `12.5%`, `1/6` → `16.7%`, `3/3` → `100.0%`.
- Standard library only; no mutation, filesystem, network, or global state.

The Engineer must mechanically extract, compile, and test the returned
function before integration. Maximum GPU calls: 2, with one exact failure
feedback repair permitted. The Engineer must record the exact model,
`/api/chat` transport, thinking mode, prompt shape, attempts, returned code,
and any post-generation integration edits.

## Acceptance

The integrated outcome report must include a deterministic success-rate line
using the GPU-produced helper, preserve all prior behavior, pass focused and
full ANVIL tests, and pass `git diff --check`. Axiom owns reconciliation,
acceptance, Git, and Auditor submission.
