"""Bounded primitives for deterministic benchmark run bundles."""

from anvil.manifest import _normalize_consistently
from anvil.outcome_report import render_outcome_report


def build_bundle_summary(records: list[dict[str, object]]) -> str:
    """Return the deterministic Markdown summary for one source record list.

    Records are normalized and consistency-checked before rendering.  The
    normalized outcomes are passed directly to the established report helper,
    keeping its ordering, formatting, and failure semantics unchanged while
    leaving a narrow seam for later bundle artifacts.
    """
    if not isinstance(records, list) or not records:
        raise ValueError("records must be a non-empty list")

    outcomes = tuple(_normalize_consistently(record) for record in records)
    return render_outcome_report(outcomes)
