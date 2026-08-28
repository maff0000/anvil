import unittest

from anvil.metrics import percentile


class PercentileTests(unittest.TestCase):
    def test_unsorted_input_is_sorted_for_selection(self):
        self.assertEqual(percentile([3.0, 1.0, 2.0], 0.5), 2.0)

    def test_zero_percentile_returns_minimum(self):
        self.assertEqual(percentile([4.0, 2.0, 9.0], 0.0), 2.0)

    def test_one_percentile_returns_maximum(self):
        self.assertEqual(percentile([4.0, 2.0, 9.0], 1.0), 9.0)

    def test_interior_percentile_uses_nearest_rank(self):
        self.assertEqual(percentile([10.0, 20.0, 30.0, 40.0, 50.0], 0.41), 30.0)

    def test_duplicates_are_preserved(self):
        self.assertEqual(percentile([1.0, 2.0, 2.0, 4.0], 0.75), 2.0)

    def test_input_is_not_mutated(self):
        values = [3.0, 1.0, 2.0]
        original = values.copy()
        percentile(values, 0.5)
        self.assertEqual(values, original)

    def test_empty_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            percentile([], 0.5)

    def test_invalid_percentile_raises_value_error(self):
        for p in (-0.1, 1.1, float("nan"), float("inf")):
            with self.subTest(p=p):
                with self.assertRaises(ValueError):
                    percentile([1.0], p)

    def test_non_finite_values_raise_value_error(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    percentile([1.0, value], 0.5)


if __name__ == "__main__":
    unittest.main()
