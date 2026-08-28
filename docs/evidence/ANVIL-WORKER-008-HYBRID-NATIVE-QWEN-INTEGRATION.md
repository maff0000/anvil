# ANVIL-WORKER-008 — Hybrid Native Qwen Integration

## Result

Classification: **HYBRID_NATIVE_QWEN_VIABLE**.

One fresh native in-session Engineer used one bounded, GPU-backed Qwen coding
subtask, mechanically rejected its first artifact, accepted its second
artifact, integrated it without semantic rewriting, and restored production
vLLM. A fresh native Auditor returned `AUDIT_VERDICT: GREEN`. This is one
successful bounded feature and is therefore classified VIABLE, not STRONG.

## Contract and decomposition

The predeclared contract is [ANVIL-WORKER-008-DECOMPOSITION.md](ANVIL-WORKER-008-DECOMPOSITION.md).
The useful feature was adding a deterministic success-rate line to the
existing outcome report. The Engineer owned `anvil/outcome_report.py`,
`tests/test_outcome_report.py`, and worker-008 raw evidence only. Qwen was
given no repository context and was asked only for
`format_success_rate(numerator: int, denominator: int) -> str` with the exact
WORKER-007 contract and examples. Maximum Qwen calls was two.

## Native Engineer and GPU execution

Engineer substrate: one fresh native in-session Codex Engineer, with no
external Codex process and no Git authority. One fresh native Auditor was
spawned after reconciliation.

The Engineer recorded the production baseline, stopped only `local-ai-vllm`,
loaded `qwen3.5:35b` Q4_K_M through native Ollama `/api/chat` with
`think=false`, temperature `0`, `num_predict=256`, and obtained positive GPU
evidence. `/api/ps` reported 26,824,995,456 bytes of VRAM and container
`nvidia-smi` reported the Ollama process using 25,904 MiB on the RTX 5090.

Attempt 1 compiled and passed invalid-input checks but failed every percentage
example because it omitted multiplication by 100 (for example `1/8` produced
`0.1%`). It was preserved as RED. Attempt 2 received only the unchanged
contract plus those exact mechanical failures and produced the corrected
Decimal round-half-even implementation. It compiled and passed all 8 output
examples, including the required cases and additional tie cases, plus 10/10
invalid-input cases. No third call occurred.

The exact requests, raw response bodies, extracted artifacts, metadata, GPU
snapshots, and mechanical results are preserved under
[`docs/evidence/raw/worker-008/`](raw/worker-008/). The integrated source
retains the attempt-2 function logic exactly; the Engineer made only the
report integration and tests, with no semantic edits to generated logic.

## Production and reconciliation

The Engineer unloaded Qwen and restarted the original `local-ai-vllm`
container without changing its configuration. Restoration evidence reports
HTTP 200 for the published port 8010 health endpoint, the expected
`NVFP4/Qwen3-30B-A3B-Instruct-2507-FP4` model, the expected revision
`585a2c9e794deb856281697ca21a1c5090157b85`, and RTX 5090 vLLM residency.
LiteLLM remained reachable and returned its expected unauthenticated 401
without exposing credentials.

One evidence limitation is recorded rather than concealed: the baseline
collector queried the container's internal port 8000 from the host and marked
health/model unreachable. The later restoration check correctly used the
published host port 8010 and was GREEN. This does not undermine the measured
restoration, but the baseline health fields are not a valid host-side health
measurement.

Axiom independently inspected scope and diff, ran the focused report tests,
full pytest (`45 passed, 54 subtests`), `./ops/validate` (`35` tests), and
`git diff --check`. The fresh Auditor found the implementation, Qwen contract,
integration, evidence, and production restoration GREEN with high confidence
and required no repairs.

## Final evidence

- Engineer invocations: 1
- Auditor invocations: 1
- Repair rounds: 0
- Qwen calls: 2
- Production impact: controlled stop/start only; configuration and routing unchanged
- Final tests: GREEN

## Governance lessons

The useful controls were explicit file scope, bounded Qwen calls, mechanical
artifact evaluation, lossless raw evidence, Axiom-owned reconciliation/Git,
fresh independent audit, and a hard production-restoration gate. The raw
evidence requirement directly addresses the evidence-loss failure observed in
WORKER-005.

No new broker, Redis schema, provider abstraction, scheduler, lease, sandbox,
or workflow machinery was needed. Qwen remained a bounded capability under a
native Engineer; the Engineer remained the integration authority. A single
feature does not justify broader architecture.
