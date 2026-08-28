# Capability matrix

| Capability | Evidence | Status |
|---|---|---|
| CODE-001 Qwen3.5 35B | 100/100 sequential and 100/100 at concurrency 1/2/4 | STRONG_LOCAL_CODER |
| CODE-002 bounded repair | 90/100 across 10 repair classes | REPAIR_CAPABILITY_VIABLE |
| CODE-003 bounded convergence | 96/96 GREEN; 100% first repair | STRONG_LOCAL_CONVERGENCE |
| Qwen3-Coder 30B FP4 | 21/30 CODE-001 | PROMISING |
| Current Qwen3 control | 12/50 CODE-001 | REJECTED |
| GLM-4.7-Flash NVFP4 / GPT-OSS 20B | Loaded but failed Stage-0 output integrity | REJECTED |
| Qwen3-Coder-Next / Devstral Small 2 | Not run locally | UNTESTED |
| Kimi / MiniMax / large GLM candidates | Practical single-host deployment infeasible | REJECTED FOR DEPLOYMENT |
| External fresh Codex worker process | WORKER-001: managed in-process app-server initialization failed with read-only runtime state | REJECTED_CURRENT_RUNTIME |
| Native in-session Codex subagent | WORKER-002: one bounded Engineer → PL reconciliation → fresh Auditor cycle completed GREEN | NATIVE_SUBAGENT_VIABLE |
| Native multi-Engineer decomposition/integration | WORKER-004: two scoped Engineers, two bounded repairs, fresh final Auditor GREEN | NATIVE_MULTI_ENGINEER_VIABLE |
| Native Engineer + bounded local GPU delegation | WORKER-005: two bounded artifacts; second failed corrected exact-rounding case; no integration | LOCAL_GPU_DELEGATION_REJECTED_RUNTIME_UNVERIFIED |
| Local GPU runtime re-proof | WORKER-006 historical shell view was sandbox-isolated; current container evidence proves NVIDIA runtime, while Ollama Qwen use remains unverified | NVIDIA_RUNTIME_VERIFIED_SANDBOX_ISOLATED / OLLAMA_QWEN_GPU_BACKING_UNVERIFIED |
| Exclusive Ollama Qwen re-proof | WORKER-007: one exact Qwen3.5 Q4_K_M call passed with 26.8 GB Ollama VRAM residency; production restored | OLLAMA_QWEN_GPU_BACKING_VERIFIED / LOCAL_QWEN_CONTRACT_VIABLE |

Raw benchmark corpora remain local under `results/`; ignored output is
evidence, not application logic.
