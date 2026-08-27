from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path
import time
from typing import Callable
from urllib import request

from .contracts import Benchmark
from .evaluation import evaluate
from .models import InferenceResponse, RuntimeConfig


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def infer(config: RuntimeConfig, prompt: str) -> InferenceResponse:
    payload = {"model": config.model, "messages": [{"role": "user", "content": prompt}], "temperature": config.temperature, "max_tokens": config.output_tokens}
    if config.think is not None:
        payload["think"] = config.think
    body = json.dumps(payload).encode()
    headers = {"Content-Type": "application/json"}
    if config.api_key:
        headers["Authorization"] = "Bearer " + config.api_key
    req = request.Request(config.endpoint.rstrip("/") + "/chat/completions", data=body, headers=headers, method="POST")
    with request.urlopen(req, timeout=config.timeout_seconds) as response:
        data = json.loads(response.read())
    choice = data["choices"][0]
    usage = data.get("usage") or {}
    details = usage.get("completion_tokens_details") or {}
    message = choice.get("message") or {}
    return InferenceResponse(message.get("content") or "", data.get("model", ""), usage.get("prompt_tokens"), usage.get("completion_tokens"), details.get("reasoning_tokens"), usage.get("total_tokens"), choice.get("finish_reason"), data)


def one_attempt(benchmark: Benchmark, config: RuntimeConfig, sample: int, mode: str) -> dict[str, object]:
    start = utc_now(); tick = time.monotonic()
    record: dict[str, object] = {"benchmark": benchmark.benchmark_id, "sample": sample, "mode": mode, "model": config.model, "phase": "inference", "start_utc": start}
    try:
        response = infer(config, benchmark.prompt + "\n\n## Contract\n" + benchmark.task_contract)
        result = evaluate(response.text, benchmark.reference_tests, min(5.0, benchmark.timeout_seconds))
        record.update({"actual_model": response.actual_model, "prompt_tokens": response.prompt_tokens, "output_tokens": response.output_tokens, "reasoning_tokens": response.reasoning_tokens, "total_tokens": response.total_tokens, "finish_reason": response.finish_reason, "raw_response": response.raw_response, "raw_artifact": response.text, "syntactic_validity": result.syntactic_validity, "semantic_pass": result.semantic_pass, "evaluator": result.tests, "error": result.error})
    except Exception as exc:
        record.update({"actual_model": None, "raw_artifact": "", "syntactic_validity": False, "semantic_pass": False, "evaluator": {"passed": 0, "failed": 0}, "error": f"{type(exc).__name__}: {exc}"})
    record.update({"end_utc": utc_now(), "wall_seconds": round(time.monotonic() - tick, 6), "status": "pass" if record["semantic_pass"] else "fail"})
    return record


def run(benchmark: Benchmark, config: RuntimeConfig, samples: int, mode: str, concurrency: int, emit: Callable[[dict[str, object]], None]) -> float:
    started = time.monotonic()
    if mode == "sequential":
        for sample in range(1, samples + 1): emit(one_attempt(benchmark, config, sample, mode))
    else:
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = [pool.submit(one_attempt, benchmark, config, sample, mode) for sample in range(1, samples + 1)]
            for future in as_completed(futures): emit(future.result())
    return time.monotonic() - started
