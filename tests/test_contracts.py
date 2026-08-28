from pathlib import Path

import pytest

from anvil.contracts import load_benchmark, parse_sample_count


@pytest.mark.parametrize(
    ("value", "expected"),
    [("1", 1), ("008", 8), ("100000", 100000)],
)
def test_parse_sample_count_accepts_ascii_decimal_strings(value, expected):
    assert parse_sample_count(value) == expected


@pytest.mark.parametrize(
    "value",
    ["", " 8", "8 ", "8.0", "+8", "-8", "0", "100001", "１２", "8\t"],
)
def test_parse_sample_count_rejects_invalid_strings(value):
    with pytest.raises(ValueError):
        parse_sample_count(value)


@pytest.mark.parametrize("value", [None, 8, True])
def test_parse_sample_count_rejects_non_strings(value):
    with pytest.raises(ValueError):
        parse_sample_count(value)


def _write_benchmark(directory: Path, sample_count: str | None = None) -> Path:
    (directory / "contract.md").write_text("contract", encoding="utf-8")
    (directory / "prompt.txt").write_text("prompt", encoding="utf-8")
    (directory / "reference_tests.py").write_text("# tests", encoding="utf-8")
    optional = f"sample_count: \"{sample_count}\"\n" if sample_count is not None else ""
    path = directory / "benchmark.yaml"
    path.write_text(
        "benchmark_id: TEST\n"
        "contract: contract.md\n"
        "prompt: prompt.txt\n"
        "reference_tests: reference_tests.py\n"
        + optional,
        encoding="utf-8",
    )
    return path


def test_load_benchmark_parses_optional_sample_count(tmp_path):
    benchmark = load_benchmark(_write_benchmark(tmp_path, "008"))

    assert benchmark.sample_count == 8


def test_load_benchmark_preserves_absent_sample_count_behavior():
    benchmark = load_benchmark(Path("benchmarks/slugify/benchmark.yaml"))

    assert benchmark.sample_count is None
    assert benchmark.target_function == "slugify"
    assert benchmark.output_tokens == 160
    assert benchmark.timeout_seconds == 60


@pytest.mark.parametrize("sample_count", ["", " 8", "8.0", "+8", "0", "100001"])
def test_load_benchmark_rejects_invalid_sample_count(tmp_path, sample_count):
    with pytest.raises(ValueError):
        load_benchmark(_write_benchmark(tmp_path, sample_count))
