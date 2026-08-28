# Qwen call 2

- Endpoint: native Ollama `/api/chat`
- Model: `qwen3.5:35b`, Q4_K_M
- Parameters: `think=false`, temperature `0`, output cap `384`, stream `false`
- Timing: `1.805178s` wall; created `2026-08-28T11:06:50.07034945Z`
- Result: contract failure; final permitted call
- Failure: `decimal.getcontext().rounding = ...` mutates process-global decimal state; response also used Markdown fences rather than only a Python artifact.
- No third call and no auto-repair.
