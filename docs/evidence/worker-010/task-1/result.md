# ANVIL-WORKER-010 — Work Item 1

## Result

Implemented runtime setting validation in `RuntimeConfig`.

- `ANVIL_SAMPLES` and `ANVIL_CONCURRENCY` must parse as positive integers.
- Zero, negative, boolean, non-integer, and malformed environment values raise
  a clear `ValueError` before benchmark execution.
- Direct `RuntimeConfig` construction applies the same strict validation.
- Valid values and existing endpoint/model routing remain unchanged.
- Existing Worker-009 model identifier normalization was retained unchanged.

## Files

- `anvil/models.py`
- `tests/test_models.py`
- `docs/evidence/worker-010/task-1/result.md`
- `docs/evidence/worker-010/task-1/test-results.txt`

## Tests

- Focused: `python3 -m pytest tests/test_models.py -q` — 30 passed.
- Full: `python3 -m pytest -q` — 106 passed, 66 subtests passed.
- Validation: `./ops/validate` — passed (42 unittest tests and compileall).

## Assumptions

- Runtime configuration construction is the correct pre-run validation seam;
  the benchmark runner receives a `RuntimeConfig` only after construction.
- Strict integer validation intentionally rejects booleans and numeric-looking
  floats for direct callers, because booleans are an `int` subclass in Python.

## Blockers

None.

## Qwen usage

Qwen was not used. The recorded Work Item 1 decision is `NATIVE_ONLY`; this is
a small repository-context integration task whose acceptance is directly
covered by deterministic local tests, and no model call was needed.
