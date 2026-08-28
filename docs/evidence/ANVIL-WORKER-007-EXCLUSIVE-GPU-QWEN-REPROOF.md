# ANVIL-WORKER-007 — Exclusive-GPU Qwen re-proof

Date: 2026-08-28 UTC
Branch: `feature/worker-007-exclusive-gpu-qwen-reproof`
Final commit: `828538ed4a06ff4cfd5986dddddcdfbb24e49c06`

## Corrected prior-state interpretation

PR #11 was corrected before this run. Current truth is:

- NVIDIA runtime: `NVIDIA_RUNTIME_VERIFIED_SANDBOX_ISOLATED`;
- Ollama Qwen backing before this experiment:
  `OLLAMA_QWEN_GPU_BACKING_UNVERIFIED`;
- WORKER-006 made no Qwen inference and remains `NOT_MEASURED`.

The historical managed-shell failure is preserved as sandbox isolation, not a
host driver failure.

## Production baseline

Before the exclusive window, the existing production container was:

- name: `local-ai-vllm`;
- container ID: `aa8ba9ac26ef5a7014aa115015d24b007bff0ee655b735d40643f5df90f69901`;
- image: `vllm/vllm-openai:latest`;
- command: `vllm serve`;
- model: `NVFP4/Qwen3-30B-A3B-Instruct-2507-FP4`;
- revision: `585a2c9e794deb856281697ca21a1c5090157b85`;
- arguments: max model length 32768, GPU memory utilization 0.76,
  auto-tool-choice enabled, Hermes parser;
- API: `/health` HTTP 200 and `/v1/models` returned the expected model;
- GPU: RTX 5090, 580.159.03, 25472 MiB allocated, active
  `VLLM::EngineCore` using 25430 MiB;
- Ollama: healthy, version 0.17.7, expected Qwen model available, no model
  loaded;
- LiteLLM: root HTTP 200; unauthenticated `/health` HTTP 401 as expected.

## Exclusive GPU window

At `2026-08-28T08:30:23Z`, Axiom stopped only `local-ai-vllm` using the normal
Docker container stop operation. The process/residency disappeared and
Ollama's container-level `nvidia-smi` showed 34 MiB of 32607 MiB allocated.

No driver, kernel, CUDA, Docker, Ollama, vLLM, LiteLLM, or model configuration
was changed.

## Ollama Qwen GPU proof

The expected model was loaded through native Ollama `/api/chat` with the exact
WORKER-005 settings: `qwen3.5:35b`, Q4_K_M, `think=false`, temperature 0, and
256 output-token cap. The request and lossless raw response are preserved at
[`attempt-001.json`](/srv/codex/anvil/docs/evidence/raw/worker-007/attempt-001.json).

Positive evidence during the call:

- `/api/ps` reported `qwen3.5:35b`, Q4_K_M, and `size_vram: 26824995456`;
- container `nvidia-smi` reported the RTX 5090 at 25946 MiB used, 59% GPU
  utilization, with `/usr/bin/ollama` using 25904 MiB;
- the returned model identifier was `qwen3.5:35b`.

`OLLAMA_QWEN_GPU_BACKING: VERIFIED`

## Exact controlled contract and result

The unchanged function contract was:

`format_success_rate(numerator: int, denominator: int) -> str`

It required strict integer/range validation, one-decimal exact percentage,
round-half-even, standard-library-only behavior, and these exact examples:
`0/3 -> 0.0%`, `1/8 -> 12.5%`, `1/6 -> 16.7%`, `1/80 -> 1.2%`,
`23/80 -> 28.8%`, and `3/3 -> 100.0%`.

Attempt 1 returned an extractable function, compiled successfully, and passed
all examples and invalid-input cases. Ollama reported 208 prompt tokens, 190
output tokens, finish reason `stop`, and a 6.093-second request duration.

Because Attempt 1 was GREEN, no second call was made. Total calls: **1**.

The first local evaluation script had an evaluator bug (`tree.walk` instead of
`ast.walk`); this did not consume a model call. Axiom corrected the evaluator
offline and re-ran the exact returned artifact. The corrected mechanical result
is GREEN and is recorded in the raw evidence.

## Unload and production restoration

At `2026-08-28T08:32:33Z`, Axiom issued the normal Ollama unload request with
`keep_alive: 0`. After five seconds, `/api/ps` was empty and container
`nvidia-smi` returned to 34 MiB with no process.

At `2026-08-28T08:32:50Z`, Axiom restarted the same `local-ai-vllm`
container. `/health` returned HTTP 200 on the fifteenth two-second readiness
poll. The restored container ID, image, arguments, GPU request, mount, model,
and revision matched the baseline. Final checks showed:

- vLLM `/health`: GREEN;
- vLLM `/v1/models`: expected production model;
- RTX 5090: visible with active `VLLM::EngineCore` using 25430 MiB;
- Ollama: healthy, Qwen unloaded;
- LiteLLM root: HTTP 200;
- production restoration: **PRODUCTION_RESTORATION_GREEN**.

## WORKER-005 comparison

| Field | WORKER-005 | WORKER-007 |
|---|---|---|
| Model | `qwen3.5:35b` Q4_K_M | `qwen3.5:35b` Q4_K_M |
| Transport | Ollama `/api/chat` | Ollama `/api/chat` |
| Thinking/temperature/cap | false / 0 / 256 | false / 0 / 256 |
| Contract | same corrected contract | same corrected contract |
| GPU backing | unverified | verified, 25904 MiB Ollama process |
| Calls | 2, both failed | 1, GREEN |
| Raw evidence | incomplete | request, response, artifact, metadata, API/GPU observations preserved |
| Integration | none | none |

WORKER-007 demonstrates that the model can satisfy this bounded contract under
positive GPU backing. The different outcome means WORKER-005's failure cannot
be promoted to a general Qwen rejection. One repeat does not establish that
GPU backing alone caused the improvement; prompt/evaluator and runtime
conditions were controlled substantially but WORKER-005 lacked complete raw
evidence.

## Independent Auditor

A fresh native Auditor reviewed the corrected prior evidence, this raw call,
the mechanical result, and production restoration. It returned:

- `AUDIT_VERDICT: GREEN`;
- `gpu_backing_verified: yes`;
- `contract_comparable: yes`;
- `capability_classification_supported: yes`;
- `production_restored: yes`;
- confidence: high.

The Auditor returned the required structured verdict:

```text
AUDIT_VERDICT: GREEN
gpu_backing_verified: yes
contract_comparable: yes
capability_classification_supported: yes
production_restored: yes
findings: none
confidence: high
```

## Final classification

- Runtime: **OLLAMA_QWEN_GPU_BACKING_VERIFIED**;
- Capability: **LOCAL_QWEN_CONTRACT_VIABLE**;
- Production: **PRODUCTION_RESTORATION_GREEN**.

The capability classification is conservative: this is one successful exact
bounded task, not a statistical reliability campaign.

## Governance lessons

The exclusive-window boundary, exact settings, mechanical evaluator, per-call
lossless evidence, GPU proof, clean unload, and exact production restoration
were useful. No provider abstraction, scheduler, Redis, broker, lease system,
GPU supervisor, or routing change was needed.

The evidence gap from WORKER-005 was a real observed problem and was fixed in
this experiment. The first evaluator bug also shows that harness correctness
must be checked before interpreting model results. No new architecture is
justified by this single successful call.
