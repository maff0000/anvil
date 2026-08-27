import json
from pathlib import Path
from statistics import mean, median


def write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records), encoding="utf-8")


def write_summary(path: Path, records: list[dict[str, object]], batch_seconds: float, mode: str) -> None:
    passed = [r for r in records if r.get("semantic_pass")]
    walls = [float(r["wall_seconds"]) for r in records]
    outputs = [int(r["output_tokens"]) for r in records if isinstance(r.get("output_tokens"), int)]
    syntax = sum(not r.get("syntactic_validity") for r in records)
    semantic = sum(bool(r.get("syntactic_validity") and not r.get("semantic_pass")) for r in records)
    timeouts = sum("timeout" in str(r.get("error", "")) or r.get("finish_reason") == "length" for r in records)
    throughput = sum(outputs) / batch_seconds if batch_seconds and outputs else 0.0
    text = [f"# ANVIL {records[0].get('benchmark', '')} — {mode}", "", f"- Samples: {len(records)}", f"- Pass: {len(passed)} ({len(passed) / len(records) * 100:.1f}%)", f"- Batch wall: {batch_seconds:.3f}s", f"- Wall mean/median: {mean(walls):.3f}s / {median(walls):.3f}s", f"- Output tokens mean/median: {(mean(outputs) if outputs else 0):.1f} / {(median(outputs) if outputs else 0):.1f}", f"- Aggregate output throughput: {throughput:.1f} tokens/s", f"- Syntax failures: {syntax}", f"- Semantic/test failures: {semantic}", f"- Timeout/truncation: {timeouts}", "", "## Failure modes", ""]
    modes = sorted({str(r.get("error")) for r in records if r.get("error")})
    text.extend(f"- `{item}`" for item in modes or ["none observed"])
    path.write_text("\n".join(text) + "\n", encoding="utf-8")
