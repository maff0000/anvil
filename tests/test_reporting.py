import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from anvil.reporting import escape_markdown_text, format_failure_rate, write_jsonl, write_summary


class FormatFailureRateTests(unittest.TestCase):
    def test_formats_zero_partial_and_complete_rates(self) -> None:
        self.assertEqual(format_failure_rate(0, 4), "0.0%")
        self.assertEqual(format_failure_rate(1, 8), "12.5%")
        self.assertEqual(format_failure_rate(4, 4), "100.0%")

    def test_uses_round_half_even(self) -> None:
        self.assertEqual(format_failure_rate(1, 160), "0.6%")
        self.assertEqual(format_failure_rate(3, 160), "1.9%")

    def test_rejects_invalid_inputs(self) -> None:
        for failures, samples in ((True, 4), (1, True), (1.0, 4), (1, 4.0), (0, 0), (-1, 4), (5, 4)):
            with self.subTest(failures=failures, samples=samples):
                with self.assertRaises(ValueError):
                    format_failure_rate(failures, samples)  # type: ignore[arg-type]


class EscapeMarkdownTextTests(unittest.TestCase):
    def test_escapes_backslash_before_markdown_special_characters(self) -> None:
        self.assertEqual(
            escape_markdown_text(r"bad_[x]*`(#)\\"),
            r"bad\_\[x\]\*\`\(\#\)\\\\",
        )

    def test_preserves_other_text_newlines_and_unicode(self) -> None:
        value = "plain text\nΔ — café / : !"
        self.assertEqual(escape_markdown_text(value), value)

    def test_rejects_non_strings(self) -> None:
        for value in (None, True, 1, b"text"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    escape_markdown_text(value)  # type: ignore[arg-type]


class WriteSummaryTests(unittest.TestCase):
    def test_failure_rate_line_covers_zero_and_partial_summary_cases(self) -> None:
        base = {
            "benchmark": "demo",
            "wall_seconds": 1.0,
            "output_tokens": 2,
            "syntactic_validity": True,
            "finish_reason": "stop",
        }
        for records, expected in (
            ([{**base, "semantic_pass": True}], "- Failure rate: 0.0%"),
            ([{**base, "semantic_pass": True}, {**base, "semantic_pass": False}], "- Failure rate: 50.0%"),
        ):
            with self.subTest(expected=expected), TemporaryDirectory() as directory:
                path = Path(directory) / "summary.md"
                write_summary(path, records, 1.0, "ollama")
                self.assertIn(expected, path.read_text(encoding="utf-8"))

    def test_escapes_only_failure_mode_label_content(self) -> None:
        records = [
            {
                "benchmark": "demo_[x]",
                "semantic_pass": False,
                "wall_seconds": 1.0,
                "output_tokens": 2,
                "syntactic_validity": True,
                "error": "bad_[x]*\\`(#)",
                "finish_reason": "stop",
            }
        ]
        with TemporaryDirectory() as directory:
            path = Path(directory) / "summary.md"
            write_summary(path, records, 1.0, "ollama")
            self.assertEqual(
                path.read_text(encoding="utf-8"),
                "\n".join(
                    [
                        "# ANVIL demo_[x] — ollama",
                        "",
                        "- Samples: 1",
                        "- Pass: 0 (0.0%)",
                        "- Failure rate: 100.0%",
                        "- Batch wall: 1.000s",
                        "- Wall mean/median: 1.000s / 1.000s",
                        "- Output tokens mean/median: 2.0 / 2.0",
                        "- Aggregate output throughput: 2.0 tokens/s",
                        "- Syntax failures: 0",
                        "- Semantic/test failures: 1",
                        "- Timeout/truncation: 0",
                        "",
                        "## Failure modes",
                        "",
                        r"- `bad\_\[x\]\*\\\`\(\#\)`",
                        "",
                    ]
                ),
            )


class WriteJsonlTests(unittest.TestCase):
    def test_creates_nested_parent_and_writes_jsonl(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "evidence" / "records.jsonl"
            records = [{"text": "Δ — café", "value": 2}, {"ok": True}]

            write_jsonl(path, records)

            self.assertEqual(
                path.read_text(encoding="utf-8"),
                '{"text": "Δ — café", "value": 2}\n{"ok": true}\n',
            )

    def test_empty_records_preserve_empty_output_behavior(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "empty.jsonl"

            write_jsonl(path, [])

            self.assertTrue(path.exists())
            self.assertEqual(path.read_text(encoding="utf-8"), "")

    def test_malformed_record_fails_before_changing_prior_output(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "records.jsonl"
            write_jsonl(path, [{"prior": True}])

            with self.assertRaises(ValueError):
                write_jsonl(path, [{"new": True}, {"invalid": {1, 2}}])

            self.assertEqual(path.read_text(encoding="utf-8"), '{"prior": true}\n')

    def test_non_dictionary_record_is_rejected_before_creating_output(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "records.jsonl"

            with self.assertRaises(ValueError):
                write_jsonl(path, [{"valid": True}, "invalid"])  # type: ignore[list-item]

            self.assertFalse(path.exists())
            self.assertFalse(path.parent.exists())


if __name__ == "__main__":
    unittest.main()
