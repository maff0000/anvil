from anvil.outcome_report import render_outcome_report
from anvil.outcomes import AttemptOutcome


def outcome(
    status: str,
    syntactic_validity: bool,
    semantic_pass: bool,
    timeout_or_truncation: bool,
    wall_seconds: int | float,
    output_tokens: int,
) -> AttemptOutcome:
    return AttemptOutcome(
        status=status,
        syntactic_validity=syntactic_validity,
        semantic_pass=semantic_pass,
        timeout_or_truncation=timeout_or_truncation,
        wall_seconds=wall_seconds,
        output_tokens=output_tokens,
    )


def test_render_mixed_outcomes_and_summary() -> None:
    outcomes = [
        outcome("semantic_failure", True, False, False, 2, 20),
        outcome("accepted", True, True, False, 1.5, 10),
        outcome("syntax_failure", False, False, True, 3.25, 30),
        outcome("accepted", True, True, True, 0, 5),
    ]

    report = render_outcome_report(outcomes)

    assert "- Sample count: 4" in report
    assert "- Accepted count: 2" in report
    assert "- Syntax failure count: 1" in report
    assert "- Semantic failure count: 1" in report
    assert "- Timeout/truncation count: 2" in report
    assert "- Total output tokens: 65" in report
    assert "- Mean wall seconds: 1.687500" in report
    assert "- Median wall seconds: 1.750000" in report


def test_render_preserves_input_order() -> None:
    outcomes = [
        outcome("syntax_failure", False, False, False, 9, 90),
        outcome("accepted", True, True, False, 1, 10),
        outcome("semantic_failure", True, False, False, 5, 50),
    ]

    report = render_outcome_report(outcomes)

    assert report.index("| 1 | syntax_failure |") < report.index("| 2 | accepted |")
    assert report.index("| 2 | accepted |") < report.index("| 3 | semantic_failure |")


def test_render_rejects_empty_input() -> None:
    try:
        render_outcome_report([])
    except ValueError as error:
        assert str(error) == "outcomes must be non-empty"
    else:
        raise AssertionError("expected ValueError")


def test_render_does_not_mutate_input() -> None:
    outcomes = [outcome("accepted", True, True, False, 1, 2)]
    original = outcomes.copy()

    render_outcome_report(outcomes)

    assert outcomes == original


def test_render_format_is_deterministic() -> None:
    outcomes = [outcome("accepted", True, True, False, 1.23456789, 7)]

    assert render_outcome_report(outcomes) == render_outcome_report(outcomes)
    assert "| 1 | accepted | true | true | false | 1.234568 | 7 |" in render_outcome_report(
        outcomes
    )


def test_render_formats_very_large_integer_duration() -> None:
    duration = 10**400
    report = render_outcome_report(
        [outcome("accepted", True, True, False, duration, 7)]
    )
    formatted_duration = f"{duration}.000000"

    assert f"- Mean wall seconds: {formatted_duration}" in report
    assert f"- Median wall seconds: {formatted_duration}" in report
    assert (
        f"| 1 | accepted | true | true | false | {formatted_duration} | 7 |"
        in report
    )
