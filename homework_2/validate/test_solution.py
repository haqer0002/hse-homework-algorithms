"""Проверка примеров, предельной длины и всех небольших перестановок."""

import subprocess
import sys
import unittest
from itertools import permutations
from pathlib import Path

from .solution import validate_stack_sequences


def all_pop_orders(pushed: tuple[int, ...]) -> set[tuple[int, ...]]:
    """Перебрать все допустимые пути, выбирая между push и pop."""
    orders = set()

    def visit(index: int, stack: tuple[int, ...], output: tuple[int, ...]) -> None:
        if index == len(pushed) and not stack:
            orders.add(output)
            return
        if index < len(pushed):
            visit(index + 1, stack + (pushed[index],), output)
        if stack:
            visit(index, stack[:-1], output + (stack[-1],))

    visit(0, (), ())
    return orders


class ValidateTests(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertTrue(validate_stack_sequences([1, 2, 3, 4, 5], [1, 3, 5, 4, 2]))
        self.assertFalse(validate_stack_sequences([1, 2, 3], [3, 1, 2]))

    def test_single_element(self) -> None:
        for value in (0, -10, 10**30):
            with self.subTest(value=value):
                self.assertTrue(validate_stack_sequences([value], [value]))

    def test_same_and_reverse_order(self) -> None:
        pushed = [8, -3, 0, 12, 5]
        self.assertTrue(validate_stack_sequences(pushed, pushed[:]))
        self.assertTrue(validate_stack_sequences(pushed, pushed[::-1]))

    def test_several_pops_after_one_push(self) -> None:
        self.assertTrue(validate_stack_sequences([1, 2, 3, 4, 5], [2, 1, 5, 4, 3]))

    def test_blocked_top(self) -> None:
        self.assertFalse(validate_stack_sequences([1, 2, 3, 4, 5], [4, 3, 5, 1, 2]))

    def test_arbitrary_integer_values(self) -> None:
        self.assertTrue(validate_stack_sequences([-5, 0, 10**30, 7], [0, 7, 10**30, -5]))
        self.assertFalse(validate_stack_sequences([-5, 0, 7], [7, -5, 0]))

    def test_empty_and_different_lengths(self) -> None:
        self.assertTrue(validate_stack_sequences([], []))
        self.assertFalse(validate_stack_sequences([1], []))
        self.assertFalse(validate_stack_sequences([], [1]))
        self.assertFalse(validate_stack_sequences([1, 2], [1]))

    def test_inputs_unchanged(self) -> None:
        pushed, popped = [1, 2, 3], [2, 3, 1]
        validate_stack_sequences(pushed, popped)
        self.assertEqual(pushed, [1, 2, 3])
        self.assertEqual(popped, [2, 3, 1])

    def test_all_permutations_up_to_six_elements(self) -> None:
        for size in range(1, 7):
            pushed = tuple(range(size))
            valid_orders = all_pop_orders(pushed)
            for popped in permutations(pushed):
                with self.subTest(popped=popped):
                    self.assertEqual(
                        validate_stack_sequences(list(pushed), list(popped)),
                        popped in valid_orders,
                    )

    def test_maximum_length(self) -> None:
        pushed = list(range(100_000))
        self.assertTrue(validate_stack_sequences(pushed, pushed[:]))
        self.assertTrue(validate_stack_sequences(pushed, pushed[::-1]))
        impossible = pushed[:-3] + [99_999, 99_997, 99_998]
        self.assertFalse(validate_stack_sequences(pushed, impossible))

    def test_cli(self) -> None:
        for input_data, expected in (
            ("1 2 3 4 5\n1 3 5 4 2\n", "True\n"),
            ("1 2 3\n3 1 2\n", "False\n"),
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
