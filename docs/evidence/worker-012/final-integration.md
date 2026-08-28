# WORKER-012 final integration proof

The completed bundle was exercised as one product slice from a single source
record list through `write_run_bundle` and `verify_run_bundle`.

- Focused command: `PYTHONPATH=. pytest -q tests/test_run_bundle.py -k
  'verify_run_bundle or invalid_input_preserves_existing_valid_bundle'`
- Result: 15 passed, 16 deselected.
- Valid read-back: `test_verify_run_bundle_accepts_bundle_written_from_records`.
- Deliberate corruption: `test_verify_run_bundle_rejects_altered_artifact` and
  the schema/reference mutation tests both require verification to reject the
  changed bundle.
- Missing/malformed artifact proof: the parameterized missing-artifact and
  malformed-JSON tests reject each required artifact failure.
- Existing-bundle safety: `test_write_run_bundle_invalid_input_preserves_existing_valid_bundle`
  proves invalid source records raise before replacing the prior valid bundle.
- Full validation at integration: `PYTHONPATH=. pytest -q` — 159 passed, 94
  subtests passed; `./ops/validate` — 57 tests passed.
- Production impact: no model call, GPU window, or production service change;
  host vLLM `/health` returned HTTP 200 and `/v1/models` reported the expected
  production model.

The proof uses temporary test directories only; no generated bundle was added
to source or committed as application data.
