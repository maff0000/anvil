"""Bounded primitives for deterministic benchmark run bundles."""

import json
import os
import shutil
import tempfile
from collections.abc import Mapping
from pathlib import Path

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


def write_run_bundle(
    directory: Path, records: list[dict[str, object]]
) -> None:
    """Atomically write all deterministic artifacts for one source record set.

    Every artifact is built and serialized before the target directory is
    changed.  The temporary sibling directory makes an incomplete bundle
    unobservable; the swap also restores an existing directory if replacement
    fails.  The artifact constants and builders are intentionally kept as the
    narrow seam for the later read-back verifier.
    """
    if not isinstance(directory, Path):
        raise ValueError("directory must be a Path")

    manifest = build_result_manifest(records)
    summary = build_bundle_summary(records)
    index = build_bundle_index(records, manifest=manifest, summary=summary)
    payloads = {
        _BUNDLE_ARTIFACTS["manifest"]: _json_bytes(manifest),
        _BUNDLE_ARTIFACTS["summary"]: summary.encode("utf-8"),
        _BUNDLE_ARTIFACTS["index"]: _json_bytes(index),
    }

    parent = directory.parent
    parent.mkdir(parents=True, exist_ok=True)
    staging: Path | None = Path(
        tempfile.mkdtemp(prefix=f".{directory.name}.", dir=parent)
    )
    backup: Path | None = None
    try:
        assert staging is not None
        for name, payload in payloads.items():
            artifact = staging / name
            with artifact.open("wb") as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())

        if directory.exists():
            if not directory.is_dir():
                raise ValueError("directory must name a directory")
            backup = Path(
                tempfile.mkdtemp(prefix=f".{directory.name}.backup.", dir=parent)
            )
            backup.rmdir()
            os.replace(directory, backup)
        try:
            assert staging is not None
            os.replace(staging, directory)
            staging = None
        except BaseException:
            if backup is not None and not directory.exists():
                os.replace(backup, directory)
                backup = None
            raise
    finally:
        if staging is not None and staging.exists():
            shutil.rmtree(staging)
        if backup is not None and backup.exists():
            shutil.rmtree(backup)


def verify_run_bundle(
    directory: Path, records: list[dict[str, object]]
) -> None:
    """Verify that a directory contains the deterministic bundle for records.

    The source records are validated by the established builders before any
    artifact is read. Verification only reads the three required artifacts;
    it does not mutate the bundle or impose meaning on unrelated files.
    """
    if not isinstance(directory, Path):
        raise ValueError("directory must be a Path")
    if not directory.is_dir():
        raise ValueError("directory must name an existing directory")

    expected_manifest = build_result_manifest(records)
    expected_summary = build_bundle_summary(records)
    expected_index = build_bundle_index(
        records, manifest=expected_manifest, summary=expected_summary
    )

    manifest = _read_json_artifact(directory / _BUNDLE_ARTIFACTS["manifest"])
    index = _read_json_artifact(directory / _BUNDLE_ARTIFACTS["index"])
    summary = _read_text_artifact(directory / _BUNDLE_ARTIFACTS["summary"])

    if manifest != expected_manifest:
        raise ValueError("manifest does not match the source records")
    if summary != expected_summary:
        raise ValueError("summary does not match the source records")
    if index != expected_index:
        raise ValueError("index does not match the expected bundle schema")


def _read_json_artifact(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid JSON artifact: {path.name}") from error


def _read_text_artifact(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ValueError(f"invalid text artifact: {path.name}") from error


def _json_bytes(value: Mapping[str, object]) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
