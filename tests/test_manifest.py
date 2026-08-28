import json
from pathlib import Path

import pytest

from anvil.manifest import build_result_manifest, write_result_manifest


def attempt(**overrides):
    record = {
        "syntactic_validity": True,
        "semantic_pass": True,
        "wall_seconds": 1.0,
        "output_tokens": 10,
    }
    record.update(overrides)
    return record


def test_build_manifest_mixed_records_uses_normalized_outcomes():
    records = [
        attempt(),
        attempt(syntactic_validity=False, semantic_pass=False, finish_reason="length"),
        attempt(semantic_pass=False, error="timeout"),
    ]

    assert build_result_manifest(records) == {
        "schema": "anvil.result_manifest",
        "version": 1,
        "samples": 3,
        "accepted": 1,
        "success_classification": "partial",
        "syntax_failures": 1,
        "semantic_failures": 1,
        "timeouts_or_truncations": 2,
        "success_rate": "33.3%",
        "failure_rate": "66.7%",
    }


@pytest.mark.parametrize(
    ("records", "classification", "success_rate", "failure_rate"),
    [
        ([attempt(), attempt()], "complete", "100.0%", "0.0%"),
        ([attempt(syntactic_validity=False), attempt(semantic_pass=False)], "none", "0.0%", "100.0%"),
    ],
)
def test_build_manifest_all_success_and_all_failure(records, classification, success_rate, failure_rate):
    manifest = build_result_manifest(records)
    assert manifest["success_classification"] == classification
    assert manifest["success_rate"] == success_rate
    assert manifest["failure_rate"] == failure_rate


def test_build_manifest_rejects_malformed_and_inconsistent_records():
    invalid_records = [
        [],
        [attempt(syntactic_validity=1)],
        [attempt(semantic_pass=0)],
        [attempt(wall_seconds=float("nan"))],
        [attempt(output_tokens=-1)],
        [attempt(status="pass", semantic_pass=False)],
        [attempt(timeout_or_truncation=True)],
    ]
    for records in invalid_records:
        with pytest.raises(ValueError):
            build_result_manifest(records)


def test_writer_is_deterministic_and_has_trailing_newline(tmp_path: Path):
    records = [attempt(semantic_pass=False, wall_seconds=2, output_tokens=4), attempt()]
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"

    write_result_manifest(first, records)
    write_result_manifest(second, records)

    assert first.read_bytes() == second.read_bytes()
    assert first.read_bytes().endswith(b"\n")
    assert json.loads(first.read_text(encoding="utf-8"))["samples"] == 2


def test_integration_manifest_aggregates_existing_result_shape_and_writes_same_manifest(
    tmp_path: Path,
):
    records = [
        {
            "syntactic_validity": True,
            "semantic_pass": True,
            "wall_seconds": 1.25,
            "output_tokens": 12,
        },
        {
            "syntactic_validity": False,
            "semantic_pass": False,
            "wall_seconds": 2,
            "output_tokens": 8,
            "finish_reason": "length",
        },
        {
            "syntactic_validity": True,
            "semantic_pass": False,
            "wall_seconds": 3,
            "output_tokens": 20,
            "error": "timeout",
        },
    ]
    expected = build_result_manifest(records)
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"

    write_result_manifest(first, records)
    write_result_manifest(second, records)

    assert json.loads(first.read_text(encoding="utf-8")) == expected
    assert first.read_bytes() == second.read_bytes()


def test_invalid_input_preserves_existing_manifest(tmp_path: Path):
    path = tmp_path / "manifest.json"
    write_result_manifest(path, [attempt()])
    original = path.read_bytes()

    with pytest.raises(ValueError):
        write_result_manifest(path, [attempt(output_tokens=True)])

    assert path.read_bytes() == original
