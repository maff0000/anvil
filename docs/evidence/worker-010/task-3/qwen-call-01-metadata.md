# Qwen call 01

- Model: `qwen3.5:35b`
- Quantization: `Q4_K_M` (verified by `/api/tags` and `/api/ps`)
- Endpoint: native Ollama `/api/chat` at `127.0.0.1:11434`
- `think`: `false`
- Temperature: `0`
- Output cap: `num_predict=384`
- HTTP status: `200`
- Client timing: `6.663099` seconds
- Ollama timing: `total_duration=6662318461 ns`, `load_duration=5271747214 ns`, `eval_count=161`
- Finish: `done=true`, `done_reason=stop`
- Result: extracted artifact is contract-valid and was accepted without repair.

## GPU evidence

Initial `/api/ps` before call: `{"models":[]}`.

Immediately after the call, `/api/ps` reported `qwen3.5:35b`, digest `3460ffeede5453ead027dbd2f821b12ad0aa3de54630971993babdb2165221f7`, `quantization_level=Q4_K_M`, and `size_vram=26824995456`.

`docker exec ollama nvidia-smi` immediately after the call reported NVIDIA GeForce RTX 5090 with Ollama using `25904MiB` GPU memory.
