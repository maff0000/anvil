# ANVIL-WORKER-012 WI-1 result

- Worker: ANVIL-WORKER-012
- Work item: WI-1 — deterministic summary artifact
- Decision: NATIVE_ONLY
- Scope: Added `build_bundle_summary(records)` as the bounded summary seam.
- Design: validates one source records list with the existing attempt
  consistency boundary and delegates to `render_outcome_report` unchanged.
- Excluded: bundle index, filesystem writer, read-back verifier, and all
  runtime/provider/scheduler/broker machinery.

## Native-only rationale

This slice is repository-local integration around an existing Markdown
contract. Native implementation preserves exact ordering, formatting, and
failure semantics, and keeps the source-record boundary visible for WI-2
through WI-4. No delegated model or external machinery was needed.

## Evidence

- Focused: `PYTHONPATH=. pytest -q tests/test_run_bundle.py
  tests/test_outcome_report.py tests/test_outcome_integration.py` — 17 passed.
- Full: `PYTHONPATH=. pytest -q` — 135 passed, 94 subtests passed.
- Validation: `./ops/validate` — 57 tests passed.
- Whitespace: `git diff --check` — clean.
- Changed paths: `anvil/run_bundle.py`, `tests/test_run_bundle.py`, and this
  evidence file only.
