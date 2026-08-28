# WORKER-012 dependent work plan and path decisions

## WI-1 — deterministic summary artifact

**Depends on:** existing outcome/report helpers.

**Decision: NATIVE_ONLY**

Rationale: summary output must preserve existing Markdown ordering and failure
escaping while becoming a bundle artifact. Repository context and exact output
compatibility outweigh any isolated formatter benefit.

Allowed files: `anvil/run_bundle.py`, `tests/test_run_bundle.py`, and
`docs/evidence/worker-012/`.

Acceptance: one records input produces deterministic `summary.md` content and
the existing report semantics remain unchanged.

## WI-2 — bundle index

**Depends on:** WI-1 and existing result manifest.

**Decision: NATIVE_ONLY**

Rationale: index fields must reference the exact artifacts and schema/version
values created by the bundle; this is integration work, not an isolated Qwen
function.

Allowed files: `anvil/run_bundle.py`, `tests/test_run_bundle.py`, and
`docs/evidence/worker-012/`.

Acceptance: deterministic `index.json` names `manifest.json`, `summary.md`,
and `index.json` with stable schema/version fields.

## WI-3 — safe bundle writer

**Depends on:** WI-1 and WI-2.

**Decision: NATIVE_ONLY**

Rationale: writing several artifacts coherently, rejecting invalid records
before mutation, and preserving a prior valid bundle are filesystem sequencing
and consistency concerns. Qwen cannot own this boundary mechanically.

Allowed files: `anvil/run_bundle.py`, `tests/test_run_bundle.py`, and
`docs/evidence/worker-012/`.

Acceptance: valid bundles are written deterministically; invalid input leaves
no misleading partial bundle and preserves an existing valid bundle.

## WI-4 — read-back verifier

**Depends on:** WI-3.

**Decision: NATIVE_ONLY**

Rationale: verification must compare all on-disk artifacts with source records
and detect missing, malformed, or cross-artifact inconsistencies. This requires
the complete repository/product context and is not a safe delegated fragment.

Allowed files: `anvil/run_bundle.py`, `tests/test_run_bundle.py`, and
`docs/evidence/worker-012/`.

Acceptance: verification passes for a valid bundle and rejects deliberate
manifest, summary, index, and missing-artifact corruption without mutation.

## Sequencing and authority

WI-1 → WI-2 → WI-3 → WI-4. Axiom sequences fresh native Engineers, checks the
actual diff after every item, owns integration and Git, and routes any defect
to a fresh repair Engineer. No Qwen call is selected, so production GPU
services will not be disturbed for this slice.
