# Qwen call 02

- Model: `qwen3.5:35b` (`Q4_K_M`), native Ollama `/api/chat`
- Parameters: `think=false`, temperature `0`, output cap `384`, call `2/2`
- Result: extracted artifact passes the ASCII/format/range contract.
- Retry basis: exact mechanical failure in call 01 (`str.isdigit()` Unicode acceptance).
