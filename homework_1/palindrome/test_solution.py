"""Тесты проверки палиндрома."""

import subprocess
import sys
import unittest
from pathlib import Path

from .solution import is_palindrome


class PalindromeTests(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertTrue(is_palindrome(121))
        self.assertFalse(is_palindrome(31))

    def test_single_digit_numbers_and_zero(self) -> None:
        for number in range(10):
            with self.subTest(number=number):
                self.assertTrue(is_palindrome(number))

    def test_palindromes(self) -> None:
        for number in (11, 99, 101, 1221, 1001, 12321, 12021, 100001, 12344321):
            with self.subTest(number=number):
                self.assertTrue(is_palindrome(number))

    def test_non_palindromes(self) -> None:
        for number in (12, 123, 1231, 1002, 12031, 1234322):
            with self.subTest(number=number):
                self.assertFalse(is_palindrome(number))

    def test_numbers_ending_in_zero(self) -> None:
        for number in (10, 100, 120, 1010, 123210):
            with self.subTest(number=number):
                self.assertFalse(is_palindrome(number))

    def test_negative_numbers(self) -> None:
        for number in (-1, -121, -1221):
            with self.subTest(number=number):
                self.assertFalse(is_palindrome(number))

    def test_large_integers(self) -> None:
        self.assertTrue(is_palindrome(10**100 + 1))
        self.assertFalse(is_palindrome(10**100 + 2))

    def test_cli(self) -> None:
        for input_data, expected in (("121\n", "True\n"), ("31\n", "False\n")):
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
