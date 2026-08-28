# Delegation failures

Both permitted Qwen calls failed the full contract. Call 1 had an inverted
type guard. Call 2 corrected that guard but mutated global decimal context and
returned fenced output. The Qwen artifacts were not integrated or repaired.

The native Engineer implemented an independent local-context helper and the
renderer integration; this is not claimed as retained Qwen code or hybrid
success.
