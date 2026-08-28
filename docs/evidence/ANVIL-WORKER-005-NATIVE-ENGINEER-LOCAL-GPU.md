# ANVIL-WORKER-005 — Native Engineer + local GPU delegation

Date: 2026-08-28 UTC
Branch: `feature/worker-005-native-engineer-local-gpu`
Setup commit: `a9733e0`
Substrate: native in-session Codex Engineer using ANVIL's existing Ollama
inference primitive

## Objective and bounded contract

The Engineer was asked to use the existing local GPU capability to generate a
single pure helper, then mechanically validate and integrate it into the
existing outcome report:

`format_success_rate(numerator: int, denominator: int) -> str`

The contract required strict integer/range validation, `ValueError` for bad
inputs, exact one-decimal percentage formatting with round-half-even, and no
state or dependencies. Under that contract, `1/80` correctly rounds to
`1.2%`; `23/80` is a useful tie case that must round to `28.8%`. The integrated
report would add a deterministic success-rate line. The Engineer had only `anvil/outcome_report.py` and
`tests/test_outcome_report.py` authorized and retained Git authority with
Axiom.

## GPU invocation

- Model: `qwen3.5:35b` (Q4_K_M)
- Transport: native Ollama `/api/chat`
- Endpoint: `http://127.0.0.1:11434/api/chat`
- Thinking: disabled (`think=False`)
- Temperature: `0.0`
- Output cap: 256 tokens
- Inference attempts: 2 maximum; both were used
- Prompt shape: exact function contract, return only the Python function, no
  Markdown/explanation; second prompt included exact first failure evidence

The Engineer used the existing `anvil.runner.infer` primitive. It performed
AST function-name extraction, compilation, and contract checks before any
integration. No generated artifact passed those checks, so no GPU output was
retained in repository code.

## GPU results

Attempt 1 returned an artifact that omitted multiplication by 100; mechanical
testing observed `(1, 8) -> 0.1%` instead of `12.5%`.

Attempt 2 was a bounded repair using the exact failure evidence. The returned
function was:

```python
def format_success_rate(numerator: int, denominator: int) -> str:
    if isinstance(numerator, bool) or isinstance(denominator, bool):
        raise ValueError("numerator and denominator must be integers, not booleans")
    if not isinstance(numerator, int) or not isinstance(denominator, int):
        raise ValueError("numerator and denominator must be integers")
    if denominator <= 0:
        raise ValueError("denominator must be a positive integer")
    if numerator < 0 or numerator > denominator:
        raise ValueError("numerator must be in [0, denominator]")
    result = (numerator / denominator) * 100
    return f"{result:.1f}%"
```

The Engineer initially compared `(1, 80) -> 1.2%` against an incorrect
expected `1.3%`. That comparison was invalid under the written round-half-even
contract. Axiom re-evaluated the exact second artifact after correcting the
contract: `(1, 80) -> 1.2%` passes, while `(23, 80) -> 28.7%` fails the exact
required `28.8%` result because of binary float rounding. Thus the second
artifact still fails the complete contract, but for a corrected, mechanically
valid reason. Both artifacts compiled and were extractable. The Engineer did
not silently repair either artifact and changed no files.

Returned Ollama metadata:

| Attempt | Actual model | Finish | Prompt tokens | Output tokens |
|---:|---|---|---:|---:|
| 1 | `qwen3.5:35b` | `stop` | 173 | 186 |
| 2 | `qwen3.5:35b` | `stop` | 243 | 157 |

### Raw evidence limitation

The Engineer returned the exact second extracted artifact and a failure
description for the first artifact, plus Ollama metadata, but did not persist
the raw JSON request/response bodies to a file before the child session ended.
Those bodies are therefore unavailable for later reconstruction. This is an
evidence-preservation failure and is reported explicitly; it is not treated as
proof that the missing first response had any particular unseen content.

The Engineer reported `nvidia-smi` could not communicate with the NVIDIA
driver. GPU acceleration was therefore not independently proven during this
run; this is recorded as an operational limitation rather than inferred away.

## Engineer and Axiom result

The Engineer made no integration edits because no GPU artifact passed. Axiom
verified the actual worktree remained unchanged, reran the existing focused
and full tests, ran `./ops/validate`, and ran `git diff --check`. Existing
ANVIL behavior remained intact. No production routing/runtime/configuration
was changed.

- Focused/full baseline: 44 pytest tests passed
- `./ops/validate`: passed (35 tests)
- baseline `git diff --check`: passed before evidence documentation was added;
  the initial evidence commit itself contained trailing Markdown whitespace,
  corrected in the follow-up evidence commit
- Files changed by Engineer: none
- GPU-generated code retained: none

## Auditor and classification

Because there was no integrated candidate, a fresh Auditor was asked to
independently verify the delegation evidence and whether rejection was
warranted. The first Auditor returned `RED` for evidence incompleteness and
the false diff-check claim. Axiom corrected those issues. A second Auditor then
returned `RED` because the original evidence used the incorrect `1/80 -> 1.3%`
expectation. Axiom corrected the contract and re-evaluated the exact artifact;
the final re-audit used no further GPU call and returned `GREEN` with high
confidence. It confirmed the corrected evidence and rejection classification,
with no remaining repair findings.

Final classification: **LOCAL_GPU_DELEGATION_REJECTED**

This rejects the bounded delegation result for this exact task/runtime under a
two-call cap. It does not reject Qwen3.5's already-proven direct bounded
capabilities, native Codex subagents, or the existing ANVIL Ollama transport
outside this experiment.

## Governance lessons

Useful controls were an exact GPU contract, existing inference primitive,
mechanical extraction/compile/tests, a two-call ceiling, no silent repair,
Engineer integration authority, Axiom-owned Git, and evidence preservation.

No provider abstraction, model router, GPU agent shell, Redis, scheduler, or
retry framework was justified. The experiment exposed a capability/runtime
measurement gap—GPU acceleration could not be independently confirmed—not a
need for more governance machinery.

Exact worker lifecycle timestamps and token telemetry beyond the Ollama
response counts were not exposed by the collaboration API and are not
fabricated.
