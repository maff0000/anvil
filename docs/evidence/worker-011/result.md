# ANVIL-WORKER-011 — Native Engineer result

```text
worker_id: ANVIL-WORKER-011-END-TO-END-AUTONOMOUS-DELIVERY
work_item: deterministic campaign result manifest construction and atomic writing
path_decisions:
  subtask_a: NATIVE_ONLY
  subtask_b: NATIVE_ONLY
qwen: not used; the implementation crosses existing normalization, summary,
classification, rate-formatting, and filesystem atomicity seams, so native
repository-context work is the smallest coherent and safest implementation.
```

## Implementation

- Added `build_result_manifest` with stable `schema`/`version` metadata and
  deterministic sample, acceptance, classification, failure, timeout, success
  rate, and failure rate fields.
- Reused `normalize_attempt`, `AttemptOutcome`, `summarize_attempts`,
  `classify_success_rate`, `format_success_rate`, and `format_failure_rate`.
- Rejected empty/non-list input, malformed normalized records, and optional
  status/timeout flags inconsistent with the canonical outcome.
- Added pre-validation and deterministic sorted-key JSON serialization with a
  trailing newline, standard-library temporary-file/fsync/replace writing,
  and cleanup on failure.

## Tests and evidence

```text
focused: python3 -m pytest -q tests/test_manifest.py — 6 passed
full: python3 -m pytest -q — 127 passed, 94 subtests passed
validation: ./ops/validate — passed
whitespace: git diff --check — passed
```

`pytest -q tests/test_manifest.py` was also attempted; this checkout's direct
launcher did not place the local package on `sys.path`, so the equivalent
standard invocation `python3 -m pytest -q tests/test_manifest.py` was used and
passed.

```text
DELIVERY_STATUS: DELIVERY_CANDIDATE
HUMAN_INTERVENTION_DURING_LOOP: 0
```
