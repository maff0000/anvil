# ANVIL-WORKER-010 Work Item 5

Decision: `NATIVE_ONLY`

## Implementation

Hardened `write_jsonl` in `anvil/reporting.py` so it:

- serializes and validates every record before changing the filesystem;
- rejects non-dictionary and non-JSON-serializable records with `ValueError`;
- creates the complete intended parent directory only after validation;
- preserves existing JSONL formatting, Unicode handling, and empty-batch output.

## Scope

Changed only:

- `anvil/reporting.py`
- `tests/test_reporting.py`
- `docs/evidence/worker-010/task-5/`

No model, runtime, service, router, scheduler, Redis, provider, ACK/PBG, or
Git-authority machinery was used or modified. vLLM remained stopped and Qwen
was not used.

## Tests and results

- Focused: `python3 -m pytest -q tests/test_reporting.py` — 8 passed, 4 subtests.
- Full: `python3 -m pytest -q` — 117 passed, 85 subtests.
- Validation: `./ops/validate` — passed (53 unittest cases, `OK`).
- `git diff --check` — passed.

Coverage includes nested parent creation, empty batches, valid JSONL
preservation, malformed serializable records leaving prior output unchanged,
and non-dictionary records failing before output or parent creation.

## Assessment

The implementation was straightforward: the existing generator was replaced
with a small validation/staging pass followed by bounded parent creation and
the original write format. Qwen would have added ceremony without useful
benefit here: the contract is local, deterministic, directly testable, and
the required I/O sequencing is clear from repository context. Native-only was
appropriate because no model judgment, broad architecture, or cross-service
integration was involved, and avoiding GPU delegation kept the campaign
boundary intact.

Blockers: none.
