from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Benchmark:
    benchmark_id: str
    task_contract: str
    prompt: str
    reference_tests: Path
    output_tokens: int
    timeout_seconds: float


def load_benchmark(path: str | Path) -> Benchmark:
    location = Path(path).resolve(strict=True)
    data: dict[str, Any] = {}
    for line in location.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"').strip("'")
        data[key.strip()] = value
    if not isinstance(data, dict):
        raise ValueError("benchmark must be a mapping")
    required = {"benchmark_id", "contract", "prompt", "reference_tests"}
    missing = required - data.keys()
    if missing:
        raise ValueError(f"benchmark missing fields: {', '.join(sorted(missing))}")
    test_path = (location.parent / data["reference_tests"]).resolve(strict=True)
    if location.parent not in test_path.parents:
        raise ValueError("reference_tests must remain inside the benchmark directory")
    return Benchmark(
        benchmark_id=str(data["benchmark_id"]),
        task_contract=(location.parent / data["contract"]).read_text(encoding="utf-8"),
        prompt=(location.parent / data["prompt"]).read_text(encoding="utf-8"),
        reference_tests=test_path,
        output_tokens=int(data.get("output_tokens", 160)),
        timeout_seconds=float(data.get("timeout_seconds", 60)),
    )
