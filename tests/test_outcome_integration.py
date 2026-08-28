from anvil.outcome_report import render_outcome_report
from anvil.outcomes import normalize_attempt


def test_raw_attempts_normalize_and_render_end_to_end() -> None:
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

    outcomes = [normalize_attempt(record) for record in records]
    report = render_outcome_report(outcomes)

    assert "- Sample count: 3" in report
    assert "- Accepted count: 1" in report
    assert "- Syntax failure count: 1" in report
    assert "- Semantic failure count: 1" in report
    assert "- Timeout/truncation count: 2" in report
    assert "- Total output tokens: 40" in report
    assert "| 1 | accepted | true | true | false | 1.250000 | 12 |" in report
    assert "| 2 | syntax_failure | false | false | true | 2.000000 | 8 |" in report
    assert "| 3 | semantic_failure | true | false | true | 3.000000 | 20 |" in report
