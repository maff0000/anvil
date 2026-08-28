"""Deterministic summaries for benchmark attempt evidence."""

from collections.abc import Mapping
from decimal import Decimal
from math import isfinite


_REQUIRED_FIELDS = (
    "syntactic_validity",
    "semantic_pass",
    "wall_seconds",
    "output_tokens",
)


def summarize_attempts(records: list[dict[str, object]]) -> dict[str, object]:
    """Validate attempt records and return aggregate benchmark evidence."""
    if not records:
        raise ValueError("records must be non-empty")

    wall_seconds: list[int | float] = []
    accepted = 0
    syntax_failures = 0
    semantic_failures = 0
    timeouts_or_truncations = 0
    output_tokens_total = 0

    for record in records:
        if not isinstance(record, Mapping):
            raise ValueError("each record must be a mapping")
        if any(field not in record for field in _REQUIRED_FIELDS):
            raise ValueError("record is missing a required field")

        syntactic_validity = record["syntactic_validity"]
        semantic_pass = record["semantic_pass"]
        elapsed = record["wall_seconds"]
        output_tokens = record["output_tokens"]

        if not isinstance(syntactic_validity, bool) or not isinstance(semantic_pass, bool):
            raise ValueError("validity and pass flags must be bool")
        if isinstance(elapsed, bool) or not isinstance(elapsed, (int, float)):
            raise ValueError("wall_seconds must be a finite non-negative number")
        if isinstance(elapsed, float) and not isfinite(elapsed):
            raise ValueError("wall_seconds must be a finite non-negative number")
        if elapsed < 0:
            raise ValueError("wall_seconds must be a finite non-negative number")
        if isinstance(output_tokens, bool) or not isinstance(output_tokens, int):
            raise ValueError("output_tokens must be a non-negative int")
        if output_tokens < 0:
            raise ValueError("output_tokens must be a non-negative int")

        wall_seconds.append(elapsed)
        output_tokens_total += output_tokens
        if syntactic_validity and semantic_pass:
            accepted += 1
        elif not syntactic_validity:
            syntax_failures += 1
        else:
            semantic_failures += 1
        if record.get("finish_reason") == "length" or record.get("error") == "timeout":
            timeouts_or_truncations += 1

    ordered_wall_seconds = sorted(wall_seconds)
    middle = len(ordered_wall_seconds) // 2
    if len(ordered_wall_seconds) % 2:
        median = ordered_wall_seconds[middle]
    else:
        median = (
            _as_decimal(ordered_wall_seconds[middle - 1])
            + _as_decimal(ordered_wall_seconds[middle])
        ) / 2

    return {
        "samples": len(records),
        "accepted": accepted,
        "syntax_failures": syntax_failures,
        "semantic_failures": semantic_failures,
        "timeouts_or_truncations": timeouts_or_truncations,
        "output_tokens_total": output_tokens_total,
        "wall_seconds_mean": _finite_result(
            sum((_as_decimal(value) for value in wall_seconds), Decimal(0)) / len(wall_seconds)
        ),
        "wall_seconds_median": _finite_result(median),
    }


def _as_decimal(value: int | float | Decimal) -> Decimal:
    """Convert a validated duration without imposing float's range limit."""
    if isinstance(value, float):
        return Decimal.from_float(value)
    return Decimal(value)


def _finite_result(value: int | float | Decimal) -> int | float | Decimal:
    """Keep the established float result where possible, otherwise stay Decimal."""
    try:
        result = float(value)
    except OverflowError:
        return value
    return result if isfinite(result) else value
