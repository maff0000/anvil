# ANVIL-WORKER-006 — Local runtime re-proof

Date: 2026-08-28 UTC  
Branch: `feature/worker-006-local-runtime-reproof`  
Parent evidence: WORKER-005 at `170c6c7`  
Runtime: native Ollama, expected model `qwen3.5:35b` Q4_K_M

## Purpose and control

This was a controlled repeat of WORKER-005, not a new coding task. The exact
function contract was preserved, including strict integer validation,
round-half-even formatting, and the cases `0/3`, `1/8`, `1/6`, `1/80`,
`23/80`, and `3/3`. The two-call limit and expected model were unchanged.

No inference call was made because the intended GPU-backed runtime failed the
precondition. Running Ollama on an unverified CPU path would not answer the
controlled question.

## Runtime state

Read-only checks on the clean WORKER-006 branch produced:

- `nvidia-smi`: failed — “couldn't communicate with the NVIDIA driver”;
- `/dev/nvidia*`: no NVIDIA device nodes present;
- Ollama `/api/version`: `0.17.7` and reachable;
- Ollama `/api/ps`: reachable, no models loaded;
- Ollama `/api/tags`: expected `qwen3.5:35b` tag present;
- Ollama `/api/show` for `qwen3.5:35b`: GGUF, Q4_K_M, 36.0B parameter model;
- no driver version, GPU model, VRAM state, or positive GPU process/residency
  evidence was available.

GPU_BACKING: **UNVERIFIED**  
Runtime classification: **LOCAL_GPU_RUNTIME_BLOCKED**

The model artifact is available to Ollama, but the NVIDIA runtime/device
precondition is not operational. No driver, kernel, CUDA, container, model
server, or production service repair was attempted.

## Controlled inference

Calls made: **0**. Consequently there is no WORKER-006 attempt 1 or attempt 2,
raw response, generated artifact, token telemetry, finish reason, latency, or
mechanical result. This is intentional and preserves comparability rather than
introducing a CPU confounder.

Capability classification from WORKER-006: **NOT_MEASURED**.

WORKER-005 remains recorded as
`LOCAL_GPU_DELEGATION_REJECTED_RUNTIME_UNVERIFIED`; it is not broadened here
into a general rejection of Qwen3.5.

## Comparison with WORKER-005

| Field | WORKER-005 | WORKER-006 |
|---|---|---|
| Model | `qwen3.5:35b` Q4_K_M | `qwen3.5:35b` Q4_K_M available |
| Transport | Ollama `/api/chat` | Not invoked |
| Thinking | disabled | Not invoked |
| Temperature/cap | 0 / 256 | Unchanged contract, no call |
| Calls | 2 | 0 |
| Contract | exact shared function contract | exact shared function contract |
| GPU backing | unverified | unverified; NVIDIA runtime blocked |
| Result | two failed artifacts, no integration | no capability measurement |

WORKER-006 does not support separating model quality from runtime quality by
inference, because the GPU-backed precondition was unavailable. It does
conclusively establish that the host cannot currently provide positive GPU
backing evidence for this repeat.

## Baseline integrity

No application source, tests, model configuration, Ollama configuration,
production routing, or vLLM configuration changed. Existing baseline checks
remain green: 44 pytest tests, 35 `./ops/validate` tests, and
`git diff --check` passed.

## Independent Auditor

A fresh native Auditor reviewed the runtime evidence, corrected contract
interpretation, and comparison. It returned `GREEN` with high confidence for
the accuracy of this blocked/unverified classification. It confirmed that no
inference should be inferred from the available evidence and that no invasive
runtime repair or new governance machinery is justified.

## Governance lessons

The evidence-preservation requirement exposed by WORKER-005 is retained as a
future control: if the precondition becomes healthy, each call must persist
canonical request data, raw response, artifact, telemetry, runtime evidence,
and mechanical results. This run needed no new framework because no call was
safe to make under the controlled design.

The appropriate next action is host/runtime maintenance outside ANVIL, not a
GPU supervisor, model router, Redis layer, retry framework, or provider
abstraction. Such maintenance is explicitly out of scope for this experiment.
