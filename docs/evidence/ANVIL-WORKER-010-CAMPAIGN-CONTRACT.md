# ANVIL-WORKER-010 campaign contract

This contract is predeclared before any Engineer is spawned. The six work
items are independent, useful ANVIL enhancements with deliberately mixed task
shapes. Final execution paths are recorded immediately before each trial.

All Engineers are fresh native in-session subagents with no Git authority.
Qwen, when selected, receives only its bounded function contract and uses the
proven native Ollama path (`qwen3.5:35b`, Q4_K_M, `think=false`, temperature 0,
maximum two calls after exact mechanical failure). No routing or policy engine
is introduced.

## Work item 1 — model identifier normalization

Useful feature: harden external model-name configuration normalization.
Expected files: `anvil/models.py`, `tests/test_models.py`, task evidence.
Acceptance: whitespace normalization is deterministic, invalid values are
rejected, and `RuntimeConfig.from_environment` behavior remains correct.
Characteristics: pure helper with an isolated contract and mechanical tests;
expected good Qwen candidate.

## Work item 2 — benchmark loading integration

Useful feature: make optional benchmark sample-count configuration usable by
the runner without changing legacy benchmarks.
Expected files: `anvil/contracts.py`, `anvil/runner.py`, relevant tests,
task evidence.
Acceptance: absent sample count preserves existing behavior, configured count
is validated and used consistently, and runner tests remain deterministic.
Characteristics: repository-context and cross-interface integration;
expected native-only candidate.

## Work item 3 — evidence summary classification

Useful feature: expose a deterministic none/partial/complete acceptance
classification for benchmark summaries.
Expected files: `anvil/metrics.py`, `anvil/evidence_summary.py`, relevant
tests, task evidence.
Acceptance: boundary and invalid cases are covered and summary output remains
backward compatible.
Characteristics: a pure classification helper plus one existing summary seam;
ambiguous mixed task.

## Work item 4 — bounded benchmark-result parser

Useful feature: parse a compact, strict `passed/total` result field for
machine-readable evidence normalization.
Expected files: `anvil/evidence_summary.py`, relevant tests, task evidence.
Acceptance: ASCII decimal counts, separator rules, bounds, and malformed
inputs are deterministic; the helper is used only where existing evidence
already carries this field.
Characteristics: parser/normalizer with an isolatable contract; expected
Qwen candidate, but integration context is mixed.

## Work item 5 — raw evidence hardening

Useful feature: make JSONL evidence writing create its intended parent
directory and fail clearly for invalid records without corrupting prior data.
Expected files: `anvil/reporting.py`, relevant tests, task evidence.
Acceptance: existing writes remain compatible, parent creation is bounded and
safe, malformed input fails before partial output, and no model/runtime code
changes.
Characteristics: repository-context and I/O/test-hardening task; expected
native-only candidate.

## Work item 6 — deterministic report rendering enhancement

Useful feature: add a compact failure-rate line to the existing Markdown
summary while preserving ordering and escaping.
Expected files: `anvil/reporting.py`, relevant tests, task evidence.
Acceptance: zero, partial, and complete cases render correctly and existing
report content remains stable.
Characteristics: pure calculation plus integration into an existing renderer;
ambiguous mixed task.

## Campaign acceptance

Before each item, Axiom records `DECISION: NATIVE_ONLY` or
`DECISION: NATIVE_PLUS_QWEN` with concise boundedness, context, testability,
usefulness, integration, and rewrite-risk rationale. Axiom independently
reconciles each result and owns Git. Fresh Auditors assess both implementation
and decision quality. Qwen raw evidence, when used, is stored below
`docs/evidence/raw/worker-010/<work-item>/`. Production vLLM is checked on
published port 8010 before and after any single safe campaign GPU window.
