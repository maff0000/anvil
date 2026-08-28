# ANVIL-WORKER-011 — End-to-end autonomous delivery contract

## Product intent

Add a deterministic campaign result manifest to ANVIL. Given completed result
records, ANVIL must construct and write one machine-readable JSON summary for
downstream evidence and scrutiny.

Required fields are sample count, accepted count, success classification,
syntax failures, semantic failures, timeout/truncation count, success rate,
failure rate, and a stable schema/version field. Inputs must be rejected when
malformed or internally inconsistent. JSON output must be deterministic and a
failed validation must not leave a misleading partial manifest. Standard
library only; no runtime/model/provider architecture.

## Decomposition

### Subtask A — manifest construction

Expected files: `anvil/manifest.py`, `tests/test_manifest.py`.

Implement:

```python
build_result_manifest(records: list[dict[str, object]]) -> dict[str, object]
```

Reuse existing `summarize_attempts` and `format_success_rate`/classification
helpers where their semantics fit. Validate all records through the existing
normalization rules, reject empty input and inconsistent status/flag data, and
return a stable-key manifest with schema/version metadata.

### Subtask B — deterministic safe writing

Expected files: `anvil/manifest.py`, `tests/test_manifest.py`.

Implement:

```python
write_result_manifest(path: Path, records: list[dict[str, object]]) -> None
```

Build and validate the complete manifest before filesystem mutation. Emit
deterministic JSON key ordering and a trailing newline. Use only a bounded
standard-library temporary-file/replace sequence so failed validation cannot
overwrite an existing manifest with misleading content.

Because both subtasks share one small module and one acceptance boundary, one
Engineer owns the complete bounded implementation. Axiom retains Git,
acceptance, and any integration seam decisions.

## Authority boundaries

The Engineer may inspect relevant ANVIL files, edit only the declared manifest
module/test files, and run tests. It must not commit, push, change branches,
modify production services, or add architecture. Worker reports are evidence.
Axiom independently reconciles scope, semantics, tests, Git, and acceptance.
A fresh Auditor receives no Engineer reasoning and may report findings but may
not edit code.

## Initial path decisions

### Subtask A

`DECISION: NATIVE_ONLY`

Rationale: manifest semantics cross `AttemptOutcome`, `summarize_attempts`,
existing rate/classification helpers, and the new schema. Repository context
and inconsistent-input validation dominate; a Qwen pure helper would add
integration ceremony and risk duplicate semantics.

### Subtask B

`DECISION: NATIVE_ONLY`

Rationale: safe deterministic JSON writing is an I/O sequencing and atomicity
problem. The Engineer must coordinate construction, validation, existing
filesystem behavior, and tests; Qwen cannot mechanically own the repository
write boundary. No Qwen call is authorized for these subtasks.

## Acceptance boundary

Focused manifest construction/writer tests, integration coverage with existing
attempt records, full ANVIL tests, `./ops/validate`, `git diff --check`, fresh
Auditor GREEN, complete GitHub evidence, and a clean reconstructable branch.

Required final declaration:

```text
DELIVERY_STATUS: DELIVERY_CANDIDATE | DELIVERY_BLOCKED
HUMAN_INTERVENTION_DURING_LOOP: 0
```
