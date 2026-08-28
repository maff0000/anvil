"""Normalize individual benchmark attempt records."""

from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class AttemptOutcome:
    status: str
    syntactic_validity: bool
    semantic_pass: bool
    timeout_or_truncation: bool
    wall_seconds: int | float
    output_tokens: int


def normalize_attempt(record: Mapping[str, object]) -> AttemptOutcome:
    """Validate and normalize one attempt record without modifying it."""
    if not isinstance(record, Mapping):
        raise ValueError("record must be a mapping")

    required = ("syntactic_validity", "semantic_pass", "wall_seconds", "output_tokens")
    if any(field not in record for field in required):
        raise ValueError("record is missing a required field")

    syntactic_validity = record["syntactic_validity"]
    semantic_pass = record["semantic_pass"]
    wall_seconds = record["wall_seconds"]
    output_tokens = record["output_tokens"]

    if not isinstance(syntactic_validity, bool) or not isinstance(semantic_pass, bool):
        raise ValueError("validity and pass flags must be bool")
    if isinstance(wall_seconds, bool) or not isinstance(wall_seconds, (int, float)):
        raise ValueError("wall_seconds must be a finite non-negative number")
    if isinstance(wall_seconds, float) and not isfinite(wall_seconds):
        raise ValueError("wall_seconds must be a finite non-negative number")
    if wall_seconds < 0:
        raise ValueError("wall_seconds must be a finite non-negative number")
    if isinstance(output_tokens, bool) or not isinstance(output_tokens, int):
        raise ValueError("output_tokens must be a non-negative int")
    if output_tokens < 0:
        raise ValueError("output_tokens must be a non-negative int")

    if syntactic_validity and semantic_pass:
        status = "accepted"
    elif not syntactic_validity:
        status = "syntax_failure"
    else:
        status = "semantic_failure"

    timeout_or_truncation = (
        record.get("finish_reason") == "length" or record.get("error") == "timeout"
    )
    return AttemptOutcome(
        status=status,
        syntactic_validity=syntactic_validity,
        semantic_pass=semantic_pass,
        timeout_or_truncation=timeout_or_truncation,
        wall_seconds=wall_seconds,
        output_tokens=output_tokens,
    )
