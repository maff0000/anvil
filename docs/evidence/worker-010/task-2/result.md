# ANVIL-WORKER-010 — Work Item 2

## Result

Integrated optional benchmark sample-count selection into `anvil.runner.run`.

- An explicit caller `samples` value remains authoritative.
- When callers pass `samples=None`, `Benchmark.sample_count` is used when
  configured.
- Legacy benchmarks without `sample_count` fall back to `RuntimeConfig.samples`,
  preserving the established runtime default.
- `one_attempt`, inference protocols, execution modes, and benchmark loading
  validation remain unchanged.

## Files

- `anvil/runner.py`
- `ops/run-benchmark`
- `tests/test_harness.py`
- `docs/evidence/worker-010/task-2/result.md`
- `docs/evidence/worker-010/task-2/test-results.txt`

`anvil/contracts.py` required no change because `Benchmark.sample_count` and
its validated loader integration were already present.

## Tests

- Focused: `python3 -m pytest tests/test_harness.py tests/test_contracts.py -q`
  — 33 passed.
- Full: `python3 -m pytest -q` — 121 passed, 94 subtests passed.
- Validation: `./ops/validate` — unittest suite passed (57 tests); compileall
  passed.
- Scope: `git diff --check` passed; implementation changes are limited to the
  allowed Work Item 2 files/directories. Existing Work Item 1 changes were
  preserved.

## Assumptions

- `samples=None` is the runner's explicit signal to select the benchmark or
  runtime default; existing callers passing an integer retain their behavior.
- For a legacy benchmark with no `sample_count`, `RuntimeConfig.samples` is
  the appropriate existing default because the runner already receives that
  configuration and previously required callers to supply its value.

## Blockers

None. No production services were contacted or modified.

## Decision

`NATIVE_ONLY` was appropriate because the change crosses the existing
Benchmark/RuntimeConfig/runner interfaces, requires preserving legacy fallback
semantics, and is small and deterministically testable in repository context.
Delegating an isolated fragment would not reduce the integration work.
