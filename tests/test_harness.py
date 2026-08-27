import tempfile
import unittest
from pathlib import Path

from anvil.evaluation import evaluate, extract_python


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


if __name__ == "__main__": unittest.main()
