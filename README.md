# ANVIL

North star: **PID in → autonomous local-GPU delivery → independently
scrutinised product out.**

Capability first. Architecture second.

ANVIL measures direct local-model coding capability. Each sample is exactly one
HTTP inference request; generated code is extracted, compiled, and evaluated in
a disposable constrained subprocess. ANVIL does not provide model-controlled
shell access, agents, retries, orchestration, Redis, or a database.

## Quick start

```sh
python -m pip install -e .
./ops/validate
./ops/run-benchmark benchmarks/slugify/benchmark.yaml --samples 8 --mode sequential
./ops/run-benchmark benchmarks/slugify/benchmark.yaml --samples 4 --mode concurrent --concurrency 4
```

Runtime settings are CLI-configurable or may be supplied with `ANVIL_*`
environment variables. Defaults target the local vLLM service at
`http://127.0.0.1:8010/v1` and model
`NVFP4/Qwen3-30B-A3B-Instruct-2507-FP4`. No credentials are committed.

Results are JSONL attempt evidence plus a compact Markdown summary in
`results/`; generated artifacts are ignored by Git.
