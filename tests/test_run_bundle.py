import pytest

from anvil.run_bundle import build_bundle_summary


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
