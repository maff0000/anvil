from dataclasses import dataclass
from pathlib import Path
import time

from .contracts import Benchmark
from .evaluation import Evaluation, evaluate
from .models import RuntimeConfig
from .runner import infer, utc_now


@dataclass(frozen=True)
class ConvergenceTask:
    benchmark: Benchmark
    initial_source: Path
    visible_tests: Path


def feedback(result: Evaluation) -> str:
    if result.error:
        return result.error
    failures = result.tests.get("failures")
    if failures:
        return "\n".join(str(item) for item in failures)
    return f"expected all visible tests to pass; passed={result.tests.get('passed', 0)} failed={result.tests.get('failed', 0)}"


def evaluate_both(source: str, task: ConvergenceTask) -> tuple[Evaluation, Evaluation]:
    visible = evaluate(source, task.visible_tests, min(5.0, task.benchmark.timeout_seconds), task.benchmark.target_function)
    hidden = evaluate(source, task.benchmark.reference_tests, min(5.0, task.benchmark.timeout_seconds), task.benchmark.target_function)
    return visible, hidden


def run_task(task: ConvergenceTask, config: RuntimeConfig, max_repairs: int = 2) -> dict[str, object]:
    initial = task.initial_source.read_text(encoding="utf-8")
    initial_visible, initial_hidden = evaluate_both(initial, task)
    current = initial
    calls: list[dict[str, object]] = []
    started = time.monotonic()
    visible = initial_visible
    for attempt in range(1, max_repairs + 1):
        prompt = (task.benchmark.prompt + "\n\n## Contract\n" + task.benchmark.task_contract +
                  "\n\n## Current implementation\n```python\n" + current +
                  "\n```\n\n## Exact visible failing test/error\n" + feedback(visible) +
                  "\n\nReturn only the corrected function.")
        call_start = utc_now()
        tick = time.monotonic()
        try:
            response = infer(config, prompt)
            visible, hidden = evaluate_both(response.text, task)
            call = {"attempt": attempt, "start_utc": call_start, "end_utc": utc_now(), "wall_seconds": round(time.monotonic() - tick, 6), "prompt": prompt, "actual_model": response.actual_model, "prompt_tokens": response.prompt_tokens, "output_tokens": response.output_tokens, "reasoning_tokens": response.reasoning_tokens, "total_tokens": response.total_tokens, "finish_reason": response.finish_reason, "raw_response": response.raw_response, "raw_artifact": response.text, "visible_evaluation": visible.__dict__, "hidden_evaluation": hidden.__dict__, "error": None}
        except Exception as exc:
            visible = Evaluation(False, False, {"passed": 0, "failed": 0}, f"{type(exc).__name__}: {exc}")
            hidden = visible
            call = {"attempt": attempt, "start_utc": call_start, "end_utc": utc_now(), "wall_seconds": round(time.monotonic() - tick, 6), "prompt": prompt, "actual_model": None, "prompt_tokens": None, "output_tokens": None, "reasoning_tokens": None, "total_tokens": None, "finish_reason": None, "raw_response": {}, "raw_artifact": "", "visible_evaluation": visible.__dict__, "hidden_evaluation": hidden.__dict__, "error": visible.error}
        calls.append(call)
        if hidden.semantic_pass or not visible.syntactic_validity or visible.semantic_pass:
            break
        current = str(call["raw_artifact"])
    return {"benchmark": task.benchmark.benchmark_id, "target_function": task.benchmark.target_function, "initial_source": initial, "initial_visible_evaluation": initial_visible.__dict__, "initial_hidden_evaluation": initial_hidden.__dict__, "calls": calls, "final_green": bool(calls and calls[-1]["hidden_evaluation"]["semantic_pass"]), "repair_calls": len(calls), "wall_seconds": round(time.monotonic() - started, 6)}
