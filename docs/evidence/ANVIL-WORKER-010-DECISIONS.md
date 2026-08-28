# WORKER-010 Axiom execution decisions

These decisions were recorded after baseline inspection and before the first
new Engineer. They are judgment records, not an automated routing policy.

## Work item 1

**DECISION: NATIVE_ONLY**

Rationale: the isolated validation is small, but its correct integration is
tightly coupled to existing environment parsing and configuration error
semantics. A bounded Qwen call would add ceremony without reducing the
Engineer’s repository-context work; rewrite risk is low but usefulness is low.

## Work item 2

**DECISION: NATIVE_ONLY**

Rationale: sample-count behavior crosses `Benchmark`, loader, runner, and CLI
assumptions. Acceptance depends on preserving legacy benchmark behavior across
interfaces, so repository context dominates and a pure delegated fragment
would not materially reduce integration effort.

## Work item 3

**DECISION: NATIVE_PLUS_QWEN**

Rationale: the classification function is bounded, deterministic, and easily
mechanically tested; the Engineer can retain integration authority at the
existing summary seam. Qwen usefulness is high and semantic rewrite risk is
low.

## Work item 4

**DECISION: NATIVE_PLUS_QWEN**

Rationale: strict `passed/total` parsing has an isolated contract with rich
boundary tests and no repository context in the generated logic. Integration
is narrow; exact mechanical evaluation controls rewrite risk.

## Work item 5

**DECISION: NATIVE_ONLY**

Rationale: safe JSONL parent creation and no-partial-output behavior depend on
I/O sequencing and existing evidence-writing semantics. Qwen would not reduce
the surrounding test-hardening work and could obscure failure atomicity.

## Work item 6

**DECISION: NATIVE_PLUS_QWEN**

Rationale: the rate-line formatter is a bounded deterministic helper with
mechanical examples, while the Engineer retains renderer integration. It is a
genuinely mixed case: Qwen may reduce pure-function effort, but the existing
report contract makes integration context material.
