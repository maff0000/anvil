# ANVIL host NVIDIA runtime restoration

Date: 2026-08-28 UTC
Branch: `feature/worker-006-local-runtime-reproof`
Classification: **NVIDIA_RUNTIME_RESTORED_GPU_VERIFIED**

## Initial apparent failure

From the managed Axiom shell, `nvidia-smi` failed and `/dev/nvidia*` was
absent. Read-only inspection nevertheless showed PCI device `01:00.0` bound
to `nvidia`, loaded 580.159.03 modules, and `/proc/driver/nvidia/gpus` naming
an RTX 5090 with active video memory.

The shell is PID 1 inside `codex-linux-sandbox`. Its `/dev` is a restricted
read-only device namespace. This explained the apparent contradiction: the
shell could see host kernel/proc state but not the NVIDIA character devices.
No host repair was attempted.

## Host/container runtime evidence

Read-only Docker inspection showed both existing services have NVIDIA device
requests through the existing runtime:

- `ollama`: `ollama/ollama:latest`, GPU device request, healthy, port 11434;
- `local-ai-vllm`: `vllm/vllm-openai:latest`, GPU device request, port 8010,
  model `NVFP4/Qwen3-30B-A3B-Instruct-2507-FP4`, revision
  `585a2c9e794deb856281697ca21a1c5090157b85`, max model length 32768, GPU
  memory utilization 0.76.

Inside the existing `ollama` container, read-only checks showed:

- `/dev/nvidia0`, `/dev/nvidiactl`, `/dev/nvidia-uvm`, and modeset devices;
- `nvidia-smi` success;
- NVIDIA GeForce RTX 5090, driver 580.159.03, CUDA 13.0;
- 32607 MiB visible, 25472 MiB allocated at observation time.

Inside the existing `local-ai-vllm` container, read-only checks showed the
same GPU and driver plus an active `VLLM::EngineCore` using 25430 MiB. This is
positive GPU-backed production evidence. The production vLLM API returned
HTTP 200 for `/health` and `/v1/models` and the expected model identifier.

Ollama `/api/version` returned `0.17.7`; `/api/tags` contained
`qwen3.5:35b` (GGUF Q4_K_M, 36.0B); `/api/ps` was empty.

## Mutation and safety

No NVIDIA modules were reloaded. No device nodes were created. No packages,
drivers, kernel, Secure Boot state, Docker runtime, Ollama configuration,
vLLM configuration, LiteLLM routing, or production service was changed. No
reboot was required.

The production service was deliberately left running because it is healthy
and positively using the GPU. Its 25.4 GiB residency leaves insufficient
headroom for a safe Qwen3.5 35B load, so no Ollama Qwen inference was started
and no production interruption was authorized by this maintenance task.

## GPU backing verdicts

- Host NVIDIA runtime: **VERIFIED** through existing vLLM container device
  access, successful container `nvidia-smi`, and active GPU process/residency.
- Ollama-specific Qwen3.5 GPU inference: **UNVERIFIED**. The model is
  available but not loaded, and no Ollama inference was run in order to avoid
  destabilizing healthy production vLLM.

Therefore this report verifies the host/runtime path but does not claim that
Ollama Qwen inference was proven. WORKER-006 must not be considered rerun by
this maintenance task.

## Final checks

- Production vLLM: GREEN, expected model and endpoint operational;
- Ollama: GREEN health/API, expected Qwen model available but unloaded;
- RTX 5090 visibility: VERIFIED inside existing GPU-enabled containers;
- managed shell `/dev/nvidia*`: intentionally unavailable due sandbox boundary;
- reboot: not required;
- ANVIL tests: 44 pytest passed, 35 `./ops/validate` tests passed;
- `git diff --check`: passed.

## Root cause and unresolved issue

Root cause of the observed ANVIL failure was execution-context device
isolation, not a missing host driver or failed kernel module. The host runtime
and production GPU path were already healthy. The remaining unresolved item
is only positive Ollama-specific Qwen GPU-use proof, which requires a safe
exclusive GPU window or sufficient free VRAM; it is not safe to obtain while
healthy production vLLM owns the GPU.
