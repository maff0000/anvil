# ANVIL-WORKER-008-FEATURE-001

This predeclared contract records the bounded hybrid experiment before the
Engineer is spawned.

## Native Engineer

The Engineer owns a useful outcome-report enhancement: add an exact success
rate to the existing deterministic outcome summary, using a bounded function
generated and mechanically checked by Qwen3.5.

Authorised write scope:

- `anvil/outcome_report.py`
- `tests/test_outcome_report.py`
- `docs/evidence/raw/worker-008/` (runtime and per-call evidence only)

The Engineer must inspect the existing report interfaces, integrate only an
accepted Qwen artifact, add focused tests, run the full ANVIL validation, and
restore the production vLLM service before reporting completion. Git remains
the Axiom PL's responsibility.

## Qwen subtask

Generate only:

```python
format_success_rate(numerator: int, denominator: int) -> str
```

The denominator must be a positive `int` and not `bool`. The numerator must
be an `int` in `[0, denominator]` and not `bool`; invalid values raise
`ValueError`. Return an exact percentage with one decimal place and `%`, using
deterministic round-half-even. Required examples are `0/3 -> 0.0%`,
`1/8 -> 12.5%`, `1/6 -> 16.7%`, `1/80 -> 1.2%`, `23/80 -> 28.8%`, and
`3/3 -> 100.0%`. Standard library only; no filesystem, network, or global
state. The output must be code only.

Maximum Qwen calls: two, with the second allowed only after exact mechanical
failure evidence from the first.

## Acceptance

The Qwen artifact must compile and pass the complete independent contract
suite before integration. The integrated report must expose the success rate
without changing existing deterministic ordering or result semantics. Focused
tests, full ANVIL tests, `./ops/validate`, `git diff --check`, and production
vLLM restoration must be GREEN. Raw request/response, artifact, runtime/GPU
proof, and mechanical results must be preserved under the worker-008 evidence
directory.
