# Architecture

ANVIL has four thin layers: benchmark definitions; direct inference; bounded
Python evaluation; and local JSONL/Markdown reporting. Definitions hold
contracts, prompts, seed code, and authoritative tests. Inference supports
OpenAI-compatible and native Ollama endpoints. Evaluation extracts a named
function, compiles it, and runs tests in a constrained disposable subprocess.

CODE-003 adds one controller-owned loop: evaluate seed, request a replacement,
evaluate it, and optionally request one further replacement. Models never
receive shell, tools, repository access, hidden tests, or loop control.

Proven boundaries are local GPU inference, native Ollama transport, bounded
Python evaluation, evidence preservation, and Git/GitHub delivery surfaces.
Agents, queues, Redis, leases, databases, workflow engines, and production
model routing are not implemented.
