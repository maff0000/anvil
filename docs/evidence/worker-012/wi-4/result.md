# ANVIL-WORKER-012 WI-4 result

- Worker: ANVIL-WORKER-012
- Work item: WI-4 — read-only benchmark run-bundle verification
- Decision: NATIVE_ONLY
- Scope: Added `verify_run_bundle(directory, records)` and focused tests.
- Behavior: Validates source records through the existing builders, reads
  `manifest.json`, `summary.md`, and `index.json`, and requires exact
  deterministic matches for schema, version, artifact references, aggregate
  values, and rendered summary content.
- Safety: Verification performs no writes and ignores unrelated files.

## Evidence

- Focused: `PYTHONPATH=. pytest -q tests/test_run_bundle.py` — 31 passed.
- Coverage: valid bundle; each missing artifact; malformed JSON; altered
  manifest count/version; altered summary; wrong index schema/reference;
  invalid source records; unrelated files.
- Changed paths: `anvil/run_bundle.py`, `tests/test_run_bundle.py`, and this
  evidence file only.
