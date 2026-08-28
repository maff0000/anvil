# Qwen call 1

- Endpoint: native Ollama `/api/chat`
- Model: `qwen3.5:35b`, Q4_K_M
- Parameters: `think=false`, temperature `0`, output cap `384`, stream `false`
- Timing: `1.923419s` wall; created `2026-08-28T11:06:37.714767922Z`
- Result: mechanical failure
- Failure: inverted boolean guard rejects valid integer inputs and permits invalid boolean cases.
- Retry: exact mechanical failure authorized call 2/2.
