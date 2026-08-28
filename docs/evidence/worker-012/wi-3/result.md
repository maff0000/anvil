# ANVIL-WORKER-012 WI-3 result

- Worker: ANVIL-WORKER-012
- Work item: WI-3 — safe bundle writer
- Decision: NATIVE_ONLY
- Scope: Added `write_run_bundle(directory, records)` in `anvil/run_bundle.py`.
- Output: Deterministic `manifest.json`, `summary.md`, and `index.json` built
  from the same validated source record set.
- Safety: All builders and serializations complete before filesystem mutation;
  artifacts are written to a temporary sibling directory and atomically
  swapped into place. A failed validation leaves no target and preserves an
  existing valid bundle. The existing builders/constants remain the seam for
  WI-4 read-back verification.
- Excluded: WI-4 verifier and all runtime/provider/scheduler/broker machinery.

## Evidence

- Focused: `PYTHONPATH=. pytest -q tests/test_run_bundle.py` — 17 passed.
- Full: `PYTHONPATH=. pytest -q` — 145 passed, 94 subtests passed.
- Validation: `./ops/validate` — 57 tests passed.
- Whitespace: `git diff --check` — clean.
- Changed paths: `anvil/run_bundle.py`, `tests/test_run_bundle.py`, and this
  evidence file only.
