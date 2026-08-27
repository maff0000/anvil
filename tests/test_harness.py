import tempfile
import unittest
from pathlib import Path

from anvil.evaluation import evaluate, extract_python
from anvil.github_control import parse_comments


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


if __name__ == "__main__": unittest.main()
