"""Тесты максимальной чётной суммы, включая независимый полный перебор."""

import subprocess
import sys
import unittest
from itertools import combinations, product
from pathlib import Path

from .solution import max_even_sum


def brute_force_max_even_sum(numbers: tuple[int, ...]) -> int:
    """Перебрать все варианты выбора элементов небольшого массива."""
    best = 0
    for size in range(len(numbers) + 1):
        for selected in combinations(numbers, size):
            candidate = sum(selected)
            if candidate % 2 == 0:
                best = max(best, candidate)
    return best


class MaxEvenSumTests(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(max_even_sum([5, 7, 13, 2, 14]), 36)
        self.assertEqual(max_even_sum([3]), 0)

    def test_empty_and_single_element(self) -> None:
        for numbers, expected in (([], 0), ([1], 0), ([2], 2), ([9], 0), ([14], 14)):
            with self.subTest(numbers=numbers):
                self.assertEqual(max_even_sum(numbers), expected)

    def test_even_total(self) -> None:
        cases = (
            ([2, 4, 6], 12),
            ([1, 3], 4),
            ([5, 5, 2], 12),
            ([1, 1, 1, 1], 4),
        )
        for numbers, expected in cases:
            with self.subTest(numbers=numbers):
                self.assertEqual(max_even_sum(numbers), expected)

    def test_odd_total(self) -> None:
        cases = (
            ([1, 3, 5], 8),
            ([7, 7, 7], 14),
            ([9, 4, 3, 8, 5], 26),
            ([10, 1, 8], 18),
            ([11, 2, 4], 6),
            ([13, 8, 5, 3, 2], 28),
            ([1, 1, 1], 2),
        )
        for numbers, expected in cases:
            with self.subTest(numbers=numbers):
                self.assertEqual(max_even_sum(numbers), expected)

    def test_large_integers(self) -> None:
        self.assertEqual(max_even_sum([10**30 + 1, 2, 4]), 6)
        self.assertEqual(
            max_even_sum([10**30 + 1, 10**30 + 3, 2]),
            2 * 10**30 + 6,
        )

    def test_one_pass_iterator(self) -> None:
        numbers = (number for number in [9, 4, 3, 8, 5])
        self.assertEqual(max_even_sum(numbers), 26)

    def test_input_is_not_changed(self) -> None:
        numbers = [9, 4, 3, 8, 5]
        original = numbers.copy()
        max_even_sum(numbers)
        self.assertEqual(numbers, original)

    def test_against_brute_force(self) -> None:
        # Все 341 массива длиной от 0 до 4 с элементами от 1 до 4.
        for length in range(5):
            for numbers in product(range(1, 5), repeat=length):
                with self.subTest(numbers=numbers):
                    self.assertEqual(
                        max_even_sum(numbers),
                        brute_force_max_even_sum(numbers),
                    )

    def test_cli(self) -> None:
        cases = (
            ("5 7 13 2 14\n", "36\n"),
            ("3\n", "0\n"),
            ("  9   4\t3 8  5  \n", "26\n"),
            ("\n", "0\n"),
        )
        for input_data, expected in cases:
            with self.subTest(input_data=input_data):
                result = subprocess.run(
                    [sys.executable, str(Path(__file__).with_name("solution.py"))],
                    input=input_data,
                    text=True,
                    capture_output=True,
                    check=True,
                    timeout=5,
                )
                self.assertEqual(result.stdout, expected)
                self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
