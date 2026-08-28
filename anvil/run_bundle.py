"""Bounded primitives for deterministic benchmark run bundles."""

from collections.abc import Mapping

from anvil.manifest import _normalize_consistently, build_result_manifest
from anvil.outcome_report import render_outcome_report


_BUNDLE_INDEX_SCHEMA = "anvil.bundle_index"
_BUNDLE_INDEX_VERSION = 1
_BUNDLE_ARTIFACTS = {
    "manifest": "manifest.json",
    "summary": "summary.md",
    "index": "index.json",
}


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


def build_bundle_index(
    records: list[dict[str, object]],
    *,
    manifest: Mapping[str, object] | None = None,
    summary: str | None = None,
) -> dict[str, object]:
    """Return the deterministic index for one validated bundle source.

    ``manifest`` and ``summary`` may be supplied when an earlier bundle stage
    has already built them.  They are checked against the same records so the
    index cannot silently describe a different source record set.  This seam
    only constructs data; it deliberately does not write or verify files.
    """
    expected_manifest = build_result_manifest(records)
    expected_summary = build_bundle_summary(records)

    if manifest is not None:
        if not isinstance(manifest, Mapping) or dict(manifest) != expected_manifest:
            raise ValueError("manifest must match the source records")
    if summary is not None:
        if not isinstance(summary, str) or summary != expected_summary:
            raise ValueError("summary must match the source records")

    return {
        "schema": _BUNDLE_INDEX_SCHEMA,
        "version": _BUNDLE_INDEX_VERSION,
        "artifacts": dict(_BUNDLE_ARTIFACTS),
    }
