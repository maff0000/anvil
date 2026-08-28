import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from anvil.contracts import Benchmark
from anvil.evaluation import evaluate, extract_python
from anvil.github_control import parse_comments
from anvil.models import RuntimeConfig
from anvil.runner import run


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.tests = Path(__file__).parents[1] / "benchmarks/slugify/reference_tests.py"

    def test_extracts_fenced_function(self):
        self.assertIn("def slugify", extract_python("```python\ndef slugify(value: str) -> str:\n    return value\n```"))

    def test_rejects_non_code(self):
        with self.assertRaises(ValueError): extract_python("Here is an answer.")

    def test_evaluates_valid_artifact(self):
        artifact = "def slugify(value: str) -> str:\n    import re\n    return re.sub(r'[^a-z0-9]+', '-', value.strip().lower()).strip('-')\n"
        result = evaluate(artifact, self.tests)
        self.assertTrue(result.syntactic_validity)
        self.assertTrue(result.semantic_pass)

    def test_preserves_syntax_failure(self):
        result = evaluate("def slugify(:", self.tests)
        self.assertFalse(result.syntactic_validity)
        self.assertIsNotNone(result.error)

    def test_evaluates_named_repair_function(self):
        tests = Path(__file__).parents[1] / "benchmarks/repair/01_clamp/reference_tests.py"
        result = evaluate("def clamp(value: int, low: int, high: int):\n    return max(low, min(value, high))", tests, function_name="clamp")
        self.assertTrue(result.semantic_pass)

    def test_github_control_filters_and_orders_cgpt_messages(self):
        comments = [{"id": 7, "body": "AXIOM_CHECKPOINT"}, {"id": 9, "body": "CGPT_ACCEPT\naccepted"}, {"id": 8, "body": "CGPT_ACK\nok"}]
        messages = parse_comments(comments, 7)
        self.assertEqual([message.comment_id for message in messages], [8, 9])

    def test_runner_uses_benchmark_sample_count_when_samples_omitted(self):
        benchmark = Benchmark("test", "contract", "prompt", self.tests, 160, 60, sample_count=3)
        records = []

        with patch("anvil.runner.one_attempt", side_effect=lambda benchmark, config, sample, mode: {"sample": sample}):
            run(benchmark, RuntimeConfig(samples=8), None, "sequential", 1, records.append)

        self.assertEqual([record["sample"] for record in records], [1, 2, 3])

    def test_runner_honors_explicit_sample_count(self):
        benchmark = Benchmark("test", "contract", "prompt", self.tests, 160, 60, sample_count=3)
        records = []

        with patch("anvil.runner.one_attempt", side_effect=lambda benchmark, config, sample, mode: {"sample": sample}):
            run(benchmark, RuntimeConfig(samples=8), 2, "sequential", 1, records.append)

        self.assertEqual([record["sample"] for record in records], [1, 2])

    def test_runner_preserves_configured_default_for_legacy_benchmark(self):
        benchmark = Benchmark("test", "contract", "prompt", self.tests, 160, 60)
        records = []

        with patch("anvil.runner.one_attempt", side_effect=lambda benchmark, config, sample, mode: {"sample": sample}):
            run(benchmark, RuntimeConfig(samples=2), None, "sequential", 1, records.append)

        self.assertEqual([record["sample"] for record in records], [1, 2])


if __name__ == "__main__": unittest.main()
