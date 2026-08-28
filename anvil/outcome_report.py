"""Deterministic Markdown rendering for normalized attempt outcomes."""

from collections.abc import Sequence
from fractions import Fraction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from anvil.outcomes import AttemptOutcome


def render_outcome_report(outcomes: Sequence["AttemptOutcome"]) -> str:
    """Render normalized outcomes as a deterministic Markdown report.

    The input is copied into a tuple so all calculations preserve the caller's
    sequence and the table always follows the supplied order.
    """
    ordered_outcomes = tuple(outcomes)
    if not ordered_outcomes:
        raise ValueError("outcomes must be non-empty")

    wall_seconds = [outcome.wall_seconds for outcome in ordered_outcomes]
    accepted = sum(outcome.status == "accepted" for outcome in ordered_outcomes)
    syntax_failures = sum(
        outcome.status == "syntax_failure" for outcome in ordered_outcomes
    )
    semantic_failures = sum(
        outcome.status == "semantic_failure" for outcome in ordered_outcomes
    )
    timeouts_or_truncations = sum(
        outcome.timeout_or_truncation for outcome in ordered_outcomes
    )
    total_output_tokens = sum(
        outcome.output_tokens for outcome in ordered_outcomes
    )

    exact_wall_seconds = [_as_fraction(value) for value in wall_seconds]
    mean_wall_seconds = sum(exact_wall_seconds, Fraction(0)) / len(
        exact_wall_seconds
    )
    ordered_wall_seconds = sorted(exact_wall_seconds)
    middle = len(ordered_wall_seconds) // 2
    if len(ordered_wall_seconds) % 2:
        median_wall_seconds = ordered_wall_seconds[middle]
    else:
        median_wall_seconds = (
            ordered_wall_seconds[middle - 1] + ordered_wall_seconds[middle]
        ) / 2

    lines = [
        "# Outcome Report",
        "",
        "## Summary",
        "",
        f"- Sample count: {len(ordered_outcomes)}",
        f"- Accepted count: {accepted}",
        f"- Syntax failure count: {syntax_failures}",
        f"- Semantic failure count: {semantic_failures}",
        f"- Timeout/truncation count: {timeouts_or_truncations}",
        f"- Total output tokens: {total_output_tokens}",
        f"- Mean wall seconds: {_format_seconds(mean_wall_seconds)}",
        f"- Median wall seconds: {_format_seconds(median_wall_seconds)}",
        "",
        "## Outcomes",
        "",
        "| # | Status | Syntactic validity | Semantic pass | Timeout/truncation | Wall seconds | Output tokens |",
        "|---:|---|---:|---:|---:|---:|---:|",
    ]
    for index, outcome in enumerate(ordered_outcomes, start=1):
        lines.append(
            "| "
            f"{index} | {outcome.status} | "
            f"{_format_bool(outcome.syntactic_validity)} | "
            f"{_format_bool(outcome.semantic_pass)} | "
            f"{_format_bool(outcome.timeout_or_truncation)} | "
            f"{_format_seconds(outcome.wall_seconds)} | "
            f"{outcome.output_tokens} |"
        )
    return "\n".join(lines) + "\n"


def _as_fraction(value: int | float) -> Fraction:
    """Convert a validated duration without losing any numeric precision."""
    return Fraction.from_float(value) if isinstance(value, float) else Fraction(value)


def _format_seconds(value: Fraction | int | float) -> str:
    """Format a non-negative duration to six places using round-half-even."""
    exact = value if isinstance(value, Fraction) else _as_fraction(value)
    scaled, remainder = divmod(exact.numerator * 1_000_000, exact.denominator)
    if remainder * 2 > exact.denominator or (
        remainder * 2 == exact.denominator and scaled % 2
    ):
        scaled += 1
    whole, fraction = divmod(scaled, 1_000_000)
    return f"{whole}.{fraction:06d}"


def _format_bool(value: bool) -> str:
    return "true" if value else "false"
