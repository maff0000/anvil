import copy
import math
import unittest

from anvil.outcomes import AttemptOutcome, normalize_attempt


def attempt(**overrides):
    record = {
        "syntactic_validity": True,
        "semantic_pass": True,
        "wall_seconds": 1.5,
        "output_tokens": 10,
    }
    record.update(overrides)
    return record


class AttemptOutcomeTests(unittest.TestCase):
    def test_status_partitions(self):
        cases = (
            ({}, "accepted"),
            ({"syntactic_validity": False}, "syntax_failure"),
            ({"syntactic_validity": False, "semantic_pass": False}, "syntax_failure"),
            ({"semantic_pass": False}, "semantic_failure"),
        )
        for overrides, expected_status in cases:
            with self.subTest(overrides=overrides):
                self.assertEqual(normalize_attempt(attempt(**overrides)).status, expected_status)

    def test_timeout_or_truncation_requires_exact_values(self):
        for overrides in (
            {"finish_reason": "length"},
            {"error": "timeout"},
            {"finish_reason": "length", "error": "timeout"},
        ):
            with self.subTest(overrides=overrides):
                self.assertTrue(normalize_attempt(attempt(**overrides)).timeout_or_truncation)
        for overrides in (
            {},
            {"finish_reason": "stop", "error": "other"},
            {"finish_reason": "Length"},
            {"error": "Timeout"},
        ):
            with self.subTest(overrides=overrides):
                self.assertFalse(normalize_attempt(attempt(**overrides)).timeout_or_truncation)

    def test_missing_and_invalid_fields_raise_value_error(self):
        with self.assertRaises(ValueError):
            normalize_attempt([])

        for field in ("syntactic_validity", "semantic_pass", "wall_seconds", "output_tokens"):
            with self.subTest(field=field):
                record = attempt()
                del record[field]
                with self.assertRaises(ValueError):
                    normalize_attempt(record)

        invalid_values = {
            "syntactic_validity": (1, "true", None),
            "semantic_pass": (0, "false", None),
            "wall_seconds": (True, "1", -1, float("nan"), float("inf"), float("-inf")),
            "output_tokens": (True, 1.0, "10", -1),
        }
        for field, values in invalid_values.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    with self.assertRaises(ValueError):
                        normalize_attempt(attempt(**{field: value}))

    def test_input_is_not_mutated(self):
        record = attempt(metadata={"nested": ["value"]})
        original = copy.deepcopy(record)
        normalize_attempt(record)
        self.assertEqual(record, original)

    def test_large_valid_values_are_preserved_without_overflow(self):
        wall_seconds = 10**400
        outcome = normalize_attempt(attempt(wall_seconds=wall_seconds, output_tokens=10**400))
        self.assertIs(outcome.wall_seconds, wall_seconds)
        self.assertEqual(outcome.output_tokens, 10**400)

        float_duration = 1e308
        outcome = normalize_attempt(attempt(wall_seconds=float_duration))
        self.assertEqual(outcome.wall_seconds, float_duration)
        self.assertTrue(math.isfinite(outcome.wall_seconds))

    def test_result_is_frozen_attempt_outcome(self):
        outcome = normalize_attempt(attempt())
        self.assertIsInstance(outcome, AttemptOutcome)
        with self.assertRaises((AttributeError, TypeError)):
            outcome.status = "changed"


if __name__ == "__main__":
    unittest.main()
