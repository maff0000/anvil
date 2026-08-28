import json

import pytest

from anvil.manifest import build_result_manifest
from anvil.run_bundle import (
    build_bundle_index,
    build_bundle_summary,
    verify_run_bundle,
    write_run_bundle,
)


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


def test_write_run_bundle_creates_all_artifacts_from_one_record_set(tmp_path):
    records = [attempt(), attempt(semantic_pass=False)]
    bundle = tmp_path / "bundle"

    assert write_run_bundle(bundle, records) is None
    assert sorted(path.name for path in bundle.iterdir()) == [
        "index.json",
        "manifest.json",
        "summary.md",
    ]
    assert json.loads((bundle / "manifest.json").read_text()) == build_result_manifest(records)
    assert (bundle / "summary.md").read_text() == build_bundle_summary(records)
    assert json.loads((bundle / "index.json").read_text()) == build_bundle_index(records)


def test_write_run_bundle_has_deterministic_bytes(tmp_path):
    records = [attempt(), attempt(semantic_pass=False, wall_seconds=2.5)]
    first = tmp_path / "first"
    second = tmp_path / "second"

    write_run_bundle(first, records)
    write_run_bundle(second, records)

    assert {
        path.name: path.read_bytes() for path in first.iterdir()
    } == {path.name: path.read_bytes() for path in second.iterdir()}


def test_write_run_bundle_invalid_input_leaves_no_partial_output(tmp_path):
    bundle = tmp_path / "bundle"

    with pytest.raises(ValueError):
        write_run_bundle(bundle, [attempt(syntactic_validity=1)])

    assert not bundle.exists()


def test_write_run_bundle_invalid_input_preserves_existing_valid_bundle(tmp_path):
    records = [attempt(), attempt(semantic_pass=False)]
    bundle = tmp_path / "bundle"
    write_run_bundle(bundle, records)
    before = {path.name: path.read_bytes() for path in bundle.iterdir()}

    with pytest.raises(ValueError):
        write_run_bundle(bundle, [attempt(status="pass", semantic_pass=False)])

    assert {path.name: path.read_bytes() for path in bundle.iterdir()} == before


def test_verify_run_bundle_accepts_bundle_written_from_records(tmp_path):
    records = [attempt(), attempt(semantic_pass=False)]
    bundle = tmp_path / "bundle"
    write_run_bundle(bundle, records)

    assert verify_run_bundle(bundle, records) is None


@pytest.mark.parametrize("artifact", ["manifest.json", "summary.md", "index.json"])
def test_verify_run_bundle_rejects_missing_artifact(tmp_path, artifact):
    records = [attempt()]
    bundle = tmp_path / "bundle"
    write_run_bundle(bundle, records)
    (bundle / artifact).unlink()

    with pytest.raises(ValueError):
        verify_run_bundle(bundle, records)


@pytest.mark.parametrize("artifact", ["manifest.json", "index.json"])
def test_verify_run_bundle_rejects_malformed_json(tmp_path, artifact):
    records = [attempt()]
    bundle = tmp_path / "bundle"
    write_run_bundle(bundle, records)
    (bundle / artifact).write_text("{not-json", encoding="utf-8")

    with pytest.raises(ValueError):
        verify_run_bundle(bundle, records)


@pytest.mark.parametrize(
    "artifact,mutation",
    [
        ("manifest.json", lambda value: value.update({"version": 99})),
        ("manifest.json", lambda value: value.update({"samples": 99})),
        ("index.json", lambda value: value.update({"schema": "wrong"})),
        (
            "index.json",
            lambda value: value["artifacts"].update({"summary": "other.md"}),
        ),
    ],
)
def test_verify_run_bundle_rejects_wrong_schema_version_or_reference(
    tmp_path, artifact, mutation
):
    records = [attempt()]
    bundle = tmp_path / "bundle"
    write_run_bundle(bundle, records)
    value = json.loads((bundle / artifact).read_text(encoding="utf-8"))
    mutation(value)
    (bundle / artifact).write_text(json.dumps(value), encoding="utf-8")

    with pytest.raises(ValueError):
        verify_run_bundle(bundle, records)


@pytest.mark.parametrize(
    "artifact,content",
    [
        ("summary.md", "# altered\n"),
        ("manifest.json", json.dumps({"schema": "anvil.result_manifest"})),
    ],
)
def test_verify_run_bundle_rejects_altered_artifact(tmp_path, artifact, content):
    records = [attempt(), attempt(semantic_pass=False)]
    bundle = tmp_path / "bundle"
    write_run_bundle(bundle, records)
    (bundle / artifact).write_text(content, encoding="utf-8")

    with pytest.raises(ValueError):
        verify_run_bundle(bundle, records)


def test_verify_run_bundle_rejects_invalid_source_records(tmp_path):
    bundle = tmp_path / "bundle"
    write_run_bundle(bundle, [attempt()])

    with pytest.raises(ValueError):
        verify_run_bundle(bundle, [attempt(syntactic_validity=1)])


def test_verify_run_bundle_ignores_unrelated_files(tmp_path):
    records = [attempt()]
    bundle = tmp_path / "bundle"
    write_run_bundle(bundle, records)
    (bundle / "unrelated.txt").write_text("outside bundle schema", encoding="utf-8")

    assert verify_run_bundle(bundle, records) is None


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
