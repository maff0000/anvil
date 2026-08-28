import copy
import math
import unittest

from anvil.evidence_summary import parse_passed_total, summarize_attempts


def attempt(**overrides):
    record = {
        "syntactic_validity": True,
        "semantic_pass": True,
        "wall_seconds": 1.0,
        "output_tokens": 10,
    }
    record.update(overrides)
    return record


class EvidenceSummaryTests(unittest.TestCase):
    def test_parse_passed_total_accepts_valid_ascii_counts(self):
        for value, expected in (("0/1", (0, 1)), ("3/3", (3, 3)), ("03/10", (3, 10))):
            with self.subTest(value=value):
                self.assertEqual(parse_passed_total(value), expected)

    def test_parse_passed_total_rejects_malformed_or_out_of_range_values(self):
        invalid = (
            " 1/2",
            "1 /2",
            "1/2 ",
            "1",
            "1//2",
            "4/3",
            "1/0",
            "١/٢",
            "1/100001",
            "100001/100001",
            "",
            "/1",
            "1/",
        )
        for value in invalid:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_passed_total(value)

    def test_parse_passed_total_rejects_non_string_values(self):
        for value in (None, 1, b"1/2"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_passed_total(value)

    def test_valid_mixed_records(self):
        records = [
            attempt(wall_seconds=4, output_tokens=12),
            attempt(syntactic_validity=False, wall_seconds=1, output_tokens=3),
            attempt(semantic_pass=False, wall_seconds=2, output_tokens=5),
        ]
        self.assertEqual(
            summarize_attempts(records),
            {
                "samples": 3,
                "accepted": 1,
                "classify_success_rate": "partial",
                "syntax_failures": 1,
                "semantic_failures": 1,
                "timeouts_or_truncations": 0,
                "output_tokens_total": 20,
                "wall_seconds_mean": 7 / 3,
                "wall_seconds_median": 2.0,
            },
        )

    def test_accepted_requires_both_flags(self):
        records = [attempt(), attempt(syntactic_validity=False), attempt(semantic_pass=False)]
        self.assertEqual(summarize_attempts(records)["accepted"], 1)

    def test_classify_success_rate_reflects_accepted_sample_count(self):
        self.assertEqual(
            summarize_attempts([attempt(), attempt(semantic_pass=False)])[
                "classify_success_rate"
            ],
            "partial",
        )
        self.assertEqual(summarize_attempts([attempt()])["classify_success_rate"], "complete")
        self.assertEqual(
            summarize_attempts([attempt(semantic_pass=False)])["classify_success_rate"],
            "none",
        )

    def test_syntax_and_semantic_failures_are_partitioned(self):
        records = [
            attempt(syntactic_validity=False, semantic_pass=False),
            attempt(syntactic_validity=False, semantic_pass=True),
            attempt(syntactic_validity=True, semantic_pass=False),
        ]
        summary = summarize_attempts(records)
        self.assertEqual(summary["syntax_failures"], 2)
        self.assertEqual(summary["semantic_failures"], 1)

    def test_timeout_and_truncation_are_deduplicated(self):
        records = [
            attempt(finish_reason="length", error="timeout"),
            attempt(finish_reason="length"),
            attempt(error="timeout"),
            attempt(finish_reason="stop", error="other"),
        ]
        self.assertEqual(summarize_attempts(records)["timeouts_or_truncations"], 3)

    def test_mean_and_median(self):
        summary = summarize_attempts([attempt(wall_seconds=9), attempt(wall_seconds=1), attempt(wall_seconds=4)])
        self.assertEqual(summary["wall_seconds_mean"], 14 / 3)
        self.assertEqual(summary["wall_seconds_median"], 4.0)

    def test_very_large_integer_duration_is_valid(self):
        duration = 10**400
        summary = summarize_attempts([attempt(wall_seconds=duration)])
        self.assertEqual(summary["wall_seconds_mean"], duration)
        self.assertEqual(summary["wall_seconds_median"], duration)

    def test_large_finite_float_aggregates_remain_finite(self):
        summary = summarize_attempts([attempt(wall_seconds=1e308), attempt(wall_seconds=1e308)])
        self.assertTrue(math.isfinite(summary["wall_seconds_mean"]))
        self.assertEqual(summary["wall_seconds_mean"], 1e308)
        self.assertTrue(math.isfinite(summary["wall_seconds_median"]))
        self.assertEqual(summary["wall_seconds_median"], 1e308)

    def test_unsorted_input_does_not_affect_median(self):
        self.assertEqual(
            summarize_attempts([attempt(wall_seconds=10), attempt(wall_seconds=2), attempt(wall_seconds=6), attempt(wall_seconds=4)])["wall_seconds_median"],
            5.0,
        )

    def test_empty_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            summarize_attempts([])

    def test_missing_fields_raise_value_error(self):
        for field in ("syntactic_validity", "semantic_pass", "wall_seconds", "output_tokens"):
            with self.subTest(field=field):
                record = attempt()
                del record[field]
                with self.assertRaises(ValueError):
                    summarize_attempts([record])

    def test_invalid_flags_raise_value_error(self):
        for field in ("syntactic_validity", "semantic_pass"):
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    summarize_attempts([attempt(**{field: 1})])

    def test_invalid_timing_raises_value_error(self):
        for value in (True, "1", -1, float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    summarize_attempts([attempt(wall_seconds=value)])

    def test_invalid_token_counts_raise_value_error(self):
        for value in (True, 1.0, "1", -1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    summarize_attempts([attempt(output_tokens=value)])

    def test_input_and_nested_mappings_are_not_mutated(self):
        records = [attempt(metadata={"nested": ["value"]})]
        original = copy.deepcopy(records)
        summarize_attempts(records)
        self.assertEqual(records, original)


if __name__ == "__main__":
    unittest.main()
