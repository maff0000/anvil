# Qwen call 01

- Model: `qwen3.5:35b` (`Q4_K_M`), native Ollama `/api/chat`
- Parameters: `think=false`, temperature `0`, output cap `384`, call `1/2`
- Result: extracted Python artifact
- Mechanical failure: `str.isdigit()` accepts Unicode digits; contract requires ASCII digits only.
- Retry authorization: exact contract failure, one retry permitted.
