"""Deterministic JSON manifests for completed benchmark attempts."""

import json
import os
import tempfile
from pathlib import Path
from typing import Mapping

from anvil.evidence_summary import summarize_attempts
from anvil.metrics import classify_success_rate
from anvil.outcome_report import format_success_rate
from anvil.outcomes import AttemptOutcome, normalize_attempt
from anvil.reporting import format_failure_rate


_SCHEMA = "anvil.result_manifest"
_VERSION = 1


def build_result_manifest(records: list[dict[str, object]]) -> dict[str, object]:
    """Validate completed attempts and return their stable aggregate manifest."""
    if not isinstance(records, list) or not records:
        raise ValueError("records must be a non-empty list")

    outcomes = [_normalize_consistently(record) for record in records]
    summary = summarize_attempts(records)
    samples = len(outcomes)
    accepted = sum(outcome.status == "accepted" for outcome in outcomes)
    failures = samples - accepted

    # Keep this assertion close to the boundary: the manifest must never mix
    # independently computed classifications and counts.
    if summary["samples"] != samples or summary["accepted"] != accepted:
        raise ValueError("record summary is internally inconsistent")

    return {
        "schema": _SCHEMA,
        "version": _VERSION,
        "samples": samples,
        "accepted": accepted,
        "success_classification": classify_success_rate(accepted, samples),
        "syntax_failures": summary["syntax_failures"],
        "semantic_failures": summary["semantic_failures"],
        "timeouts_or_truncations": summary["timeouts_or_truncations"],
        "success_rate": format_success_rate(accepted, samples),
        "failure_rate": format_failure_rate(failures, samples),
    }


def write_result_manifest(path: Path, records: list[dict[str, object]]) -> None:
    """Atomically write a validated, deterministic JSON result manifest."""
    manifest = build_result_manifest(records)
    if not isinstance(path, Path):
        raise ValueError("path must be a Path")

    payload = json.dumps(
        manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: str | None = None
    try:
        descriptor, temporary_path = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
        )
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            try:
                os.unlink(temporary_path)
            except FileNotFoundError:
                pass


def _normalize_consistently(record: dict[str, object]) -> AttemptOutcome:
    outcome = normalize_attempt(record)
    if not isinstance(record, Mapping):
        raise ValueError("record must be a mapping")

    if "status" in record:
        status = record["status"]
        accepted_status = outcome.status == "accepted"
        if status not in (outcome.status, "pass" if accepted_status else "fail"):
            raise ValueError("record status disagrees with validity flags")

    if "timeout_or_truncation" in record:
        marker = record["timeout_or_truncation"]
        if not isinstance(marker, bool) or marker != outcome.timeout_or_truncation:
            raise ValueError("record timeout flag disagrees with timeout markers")
    return outcome
