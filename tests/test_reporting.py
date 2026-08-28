import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from anvil.reporting import escape_markdown_text, write_summary


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


if __name__ == "__main__":
    unittest.main()
