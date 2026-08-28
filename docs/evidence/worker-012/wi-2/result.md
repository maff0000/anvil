# ANVIL-WORKER-012 WI-2 result

- Worker: ANVIL-WORKER-012
- Work item: WI-2 — deterministic bundle index
- Decision: NATIVE_ONLY
- Scope: Added `build_bundle_index(records, *, manifest=None, summary=None)`.
- Output: Stable `anvil.bundle_index` schema, version `1`, and exact artifact
  references `manifest.json`, `summary.md`, and `index.json`.
- Validation: The index uses the existing result-manifest builder and the
  WI-1 summary seam. Optional prebuilt manifest/summary inputs must match the
  same validated source records.
- Excluded: Multi-file writing, read-back verification, and all
  runtime/provider/scheduler/broker machinery.

## Evidence

- Focused: `PYTHONPATH=. pytest -q tests/test_run_bundle.py` — 13 passed.
- Full: `PYTHONPATH=. pytest -q` — 141 passed, 94 subtests passed.
- Validation: `./ops/validate` — 57 tests passed.
- Whitespace: `git diff --check` — clean.
- Changed paths: `anvil/run_bundle.py`, `tests/test_run_bundle.py`, and this
  evidence file only.
