"""Примеры, границы и сравнение с перебором всех пар индексов."""

import subprocess
import sys
import unittest
from itertools import product
from pathlib import Path

from .solution import two_sum


class TwoSumTests(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(two_sum([1, 3, 4, 10], 7), (1, 2))
        self.assertEqual(two_sum([5, 5, 1, 4], 10), (0, 1))

    def test_two_elements(self) -> None:
        self.assertEqual(two_sum([10, -3], 7), (0, 1))
        self.assertEqual(two_sum([5, 5], 10), (0, 1))

    def test_same_element_cannot_be_used_twice(self) -> None:
        self.assertEqual(two_sum([3, 2, 4], 6), (1, 2))
        with self.assertRaises(ValueError):
            two_sum([3], 6)

    def test_equal_values_at_different_indices(self) -> None:
        self.assertEqual(two_sum([5, 1, 5], 10), (0, 2))

    def test_zero_and_negative_values(self) -> None:
        self.assertEqual(two_sum([-4, -1, 0, 4, 8], 0), (0, 3))
        self.assertEqual(two_sum([0, 7, 0], 0), (0, 2))
        self.assertEqual(two_sum([-8, -5, 3, 7], -13), (0, 1))

    def test_large_integers(self) -> None:
        self.assertEqual(two_sum([10**50, -10**50, 9], 0), (0, 1))

    def test_diagram_example(self) -> None:
        self.assertEqual(two_sum([8, -2, 11, 4, 7], 5), (1, 4))

    def test_long_array(self) -> None:
        arr = list(range(0, 200_000, 2)) + [1]
        self.assertEqual(two_sum(arr, 199_999), (99_999, 100_000))

    def test_input_unchanged(self) -> None:
        arr = [5, 5, 1, 4]
        two_sum(arr, 10)
        self.assertEqual(arr, [5, 5, 1, 4])

    def test_missing_pair(self) -> None:
        for arr, k in (([], 0), ([1], 2), ([1, 2, 3], 20)):
            with self.subTest(arr=arr, k=k):
                with self.assertRaises(ValueError):
                    two_sum(arr, k)

    def test_against_all_pairs(self) -> None:
        for size in range(2, 6):
            for values in product((-2, -1, 0, 1, 2), repeat=size):
                for k in range(-4, 5):
                    pairs = [
                        (i, j) for i in range(size) for j in range(i + 1, size)
                        if values[i] + values[j] == k
                    ]
                    if len(pairs) == 1:
                        with self.subTest(values=values, k=k):
                            self.assertEqual(two_sum(list(values), k), pairs[0])

    def test_cli(self) -> None:
        for input_data, expected in (
            ("1 3 4 10\n7\n", "1 2\n"),
            ("5 5 1 4\n10\n", "0 1\n"),
            ("8 -2 11 4 7\n5\n", "1 4\n"),
        ):
            with self.subTest(input_data=input_data):
                result = subprocess.run(
                    [sys.executable, str(Path(__file__).with_name("solution.py"))],
                    input=input_data, text=True, capture_output=True, check=True, timeout=5,
                )
                self.assertEqual(result.stdout, expected)
                self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
