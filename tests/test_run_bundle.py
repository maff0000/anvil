import pytest

from anvil.manifest import build_result_manifest
from anvil.run_bundle import build_bundle_index, build_bundle_summary


def attempt(**overrides):
    record = {
        "syntactic_validity": True,
        "semantic_pass": True,
        "wall_seconds": 1.0,
        "output_tokens": 10,
    }
    record.update(overrides)
    return record


def test_build_bundle_summary_is_deterministic_and_uses_existing_attempt_shape():
    records = [
        attempt(),
        attempt(syntactic_validity=False, semantic_pass=False, wall_seconds=2,
                output_tokens=8, finish_reason="length"),
        attempt(semantic_pass=False, wall_seconds=3, output_tokens=20,
                error="timeout"),
    ]

    first = build_bundle_summary(records)
    second = build_bundle_summary(records)

    assert first == second
    assert first.startswith("# Outcome Report\n\n## Summary\n")
    assert "- Sample count: 3" in first
    assert "- Accepted count: 1" in first
    assert "- Timeout/truncation count: 2" in first
    assert "| 1 | accepted | true | true | false | 1.000000 | 10 |" in first
    assert "| 2 | syntax_failure | false | false | true | 2.000000 | 8 |" in first
    assert "| 3 | semantic_failure | true | false | true | 3.000000 | 20 |" in first
    assert first.endswith("\n")


def test_build_bundle_summary_does_not_mutate_source_records():
    records = [attempt(), attempt(semantic_pass=False)]
    original = [record.copy() for record in records]

    build_bundle_summary(records)

    assert records == original


def test_build_bundle_index_has_stable_keys_and_exact_artifact_references():
    records = [attempt(), attempt(semantic_pass=False)]

    first = build_bundle_index(records)
    second = build_bundle_index(records)

    assert first == second
    assert list(first) == ["schema", "version", "artifacts"]
    assert first["schema"] == "anvil.bundle_index"
    assert first["version"] == 1
    assert first["artifacts"] == {
        "manifest": "manifest.json",
        "summary": "summary.md",
        "index": "index.json",
    }


def test_build_bundle_index_accepts_matching_existing_manifest_and_summary():
    records = [attempt(), attempt(semantic_pass=False)]

    assert build_bundle_index(
        records,
        manifest=build_result_manifest(records),
        summary=build_bundle_summary(records),
    ) == build_bundle_index(records)


@pytest.mark.parametrize(
    "manifest,summary",
    [
        ({"schema": "wrong", "version": 1}, None),
        (None, "not the generated summary"),
        ({}, build_bundle_summary([attempt()])),
    ],
)
def test_build_bundle_index_rejects_malformed_or_inconsistent_references(
    manifest, summary
):
    records = [attempt()]

    with pytest.raises(ValueError):
        build_bundle_index(records, manifest=manifest, summary=summary)


def test_build_bundle_index_uses_summary_and_manifest_dependencies(monkeypatch):
    records = [attempt()]
    calls = []

    def fake_manifest(source_records):
        calls.append("manifest")
        return {"source": source_records}

    def fake_summary(source_records):
        calls.append("summary")
        return "summary"

    monkeypatch.setattr("anvil.run_bundle.build_result_manifest", fake_manifest)
    monkeypatch.setattr("anvil.run_bundle.build_bundle_summary", fake_summary)

    assert build_bundle_index(records) == {
        "schema": "anvil.bundle_index",
        "version": 1,
        "artifacts": {
            "manifest": "manifest.json",
            "summary": "summary.md",
            "index": "index.json",
        },
    }
    assert calls == ["manifest", "summary"]


@pytest.mark.parametrize(
    "records",
    [
        [],
        None,
        [attempt(syntactic_validity=1)],
        [attempt(status="pass", semantic_pass=False)],
        [attempt(timeout_or_truncation=True)],
    ],
)
def test_build_bundle_summary_rejects_malformed_or_inconsistent_records(records):
    with pytest.raises(ValueError):
        build_bundle_summary(records)
