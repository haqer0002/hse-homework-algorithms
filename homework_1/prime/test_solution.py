"""Тесты решета и сравнение с независимой проверкой делителей."""

import subprocess
import sys
import unittest
from math import isqrt
from pathlib import Path

from .solution import count_primes


def count_primes_by_trial_division(n: int) -> int:
    """Проверить каждое число перебором делителей до его квадратного корня."""
    count = 0
    for number in range(2, n):
        if all(number % divisor != 0 for divisor in range(2, isqrt(number) + 1)):
            count += 1
    return count


class CountPrimesTests(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(count_primes(10), 4)
        self.assertEqual(count_primes(1), 0)

    def test_no_primes_below_bound(self) -> None:
        for n in (-100, -1, 0, 1, 2):
            with self.subTest(n=n):
                self.assertEqual(count_primes(n), 0)

    def test_prime_upper_bound_is_excluded(self) -> None:
        for n, expected in ((3, 1), (5, 2), (7, 3), (11, 4), (29, 9)):
            with self.subTest(n=n):
                self.assertEqual(count_primes(n), expected)

    def test_bound_just_after_prime(self) -> None:
        for n, expected in ((4, 2), (6, 3), (8, 4), (12, 5), (30, 10)):
            with self.subTest(n=n):
                self.assertEqual(count_primes(n), expected)

    def test_composite_squares(self) -> None:
        for n, expected in ((9, 4), (10, 4), (25, 9), (26, 9), (49, 15), (50, 15)):
            with self.subTest(n=n):
                self.assertEqual(count_primes(n), expected)

    def test_larger_bounds(self) -> None:
        for n, expected in ((100, 25), (1000, 168), (10000, 1229)):
            with self.subTest(n=n):
                self.assertEqual(count_primes(n), expected)

    def test_against_trial_division(self) -> None:
        for n in range(-5, 201):
            with self.subTest(n=n):
                self.assertEqual(count_primes(n), count_primes_by_trial_division(n))

    def test_cli(self) -> None:
        for input_data, expected in (("10\n", "4\n"), ("1\n", "0\n"), ("29\n", "9\n")):
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
