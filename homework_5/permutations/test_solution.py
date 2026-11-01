"""Все примеры, повторы, независимость ответов и стек рекурсивных вызовов."""

import ast
from contextlib import redirect_stdout
from io import StringIO
from itertools import permutations as reference_permutations, product
from pathlib import Path
import subprocess
import sys
import unittest

from .solution import permutations


EXAMPLE = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
FIRST_BRANCH = [
    "-> backtrack([])",
    "  -> backtrack([1])",
    "    -> backtrack([1, 2])",
    "      -> backtrack([1, 2, 3])",
    "      <- backtrack = None",
    "    <- backtrack = None",
    "    -> backtrack([1, 3])",
    "      -> backtrack([1, 3, 2])",
    "      <- backtrack = None",
    "    <- backtrack = None",
    "  <- backtrack = None",
]


class PermutationsTests(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(permutations([1, 2, 3], trace=False), EXAMPLE)
        self.assertEqual(permutations([0, 1], trace=False), [[0, 1], [1, 0]])
        self.assertEqual(permutations([1], trace=False), [[1]])

    def test_empty_array(self) -> None:
        self.assertEqual(permutations([], trace=False), [[]])

    def test_repeated_values(self) -> None:
        self.assertEqual(permutations([1, 1, 2], trace=False), [[1, 1, 2], [1, 2, 1], [2, 1, 1]])
        self.assertEqual(permutations([3, 3, 3], trace=False), [[3, 3, 3]])
        self.assertEqual(permutations([2, 1, 2], trace=False), [[2, 2, 1], [2, 1, 2], [1, 2, 2]])

    def test_unsorted_negative_zero_and_large_values(self) -> None:
        for values in ([3, 1, 2], [0, -1, 2], [10**50, -(10**50), 0]):
            result = permutations(values, trace=False)
            expected = set(reference_permutations(values))
            self.assertEqual({tuple(row) for row in result}, expected)
            self.assertEqual(len(result), len(expected))

    def test_input_unchanged(self) -> None:
        values = [3, 1, 2, 1]
        before = values.copy()
        permutations(values, trace=False)
        self.assertEqual(values, before)

    def test_result_rows_and_calls_are_independent(self) -> None:
        values = [1, 2]
        first = permutations(values, trace=False)
        first[0].append(99)
        self.assertEqual(first[1], [2, 1])
        self.assertEqual(values, [1, 2])
        self.assertEqual(permutations(values, trace=False), [[1, 2], [2, 1]])

    def test_trace_is_enabled_by_default(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            result = permutations([1, 2, 3])
        lines = output.getvalue().splitlines()
        self.assertEqual(result, EXAMPLE)
        self.assertEqual(lines[:11], FIRST_BRANCH)
        self.assertEqual(len(lines), 32)
        self.assertEqual(lines[-1], "<- backtrack = None")

    def test_trace_matches_the_call_stack(self) -> None:
        for values in ([], [1], [1, 2, 3], [1, 1, 2]):
            output = StringIO()
            with redirect_stdout(output):
                result = permutations(values)
            stack = []
            leaves = []
            for line in output.getvalue().splitlines():
                spaces = len(line) - len(line.lstrip())
                if line.lstrip().startswith("->"):
                    self.assertEqual(spaces, 2 * len(stack))
                    path = ast.literal_eval(line.strip()[len("-> backtrack("):-1])
                    self.assertEqual(len(path), len(stack))
                    if stack:
                        self.assertEqual(path[:-1], stack[-1])
                    stack.append(path)
                    if len(path) == len(values):
                        leaves.append(path)
                else:
                    self.assertTrue(stack)
                    self.assertEqual(spaces, 2 * (len(stack) - 1))
                    self.assertEqual(line.strip(), "<- backtrack = None")
                    stack.pop()
            self.assertEqual(stack, [])
            self.assertEqual(leaves, result)

    def test_trace_can_be_disabled(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            result = permutations([1, 2], trace=False)
        self.assertEqual(output.getvalue(), "")
        self.assertEqual(result, [[1, 2], [2, 1]])

    def test_all_small_arrays_against_standard_library(self) -> None:
        count = 0
        for size in range(6):
            for values in product((-1, 0, 1), repeat=size):
                expected = set(reference_permutations(values))
                result = permutations(list(values), trace=False)
                with self.subTest(values=values):
                    self.assertEqual({tuple(row) for row in result}, expected)
                    self.assertEqual(len(result), len(expected))
                count += 1
        self.assertEqual(count, 364)

    def test_seven_distinct_values(self) -> None:
        result = permutations(list(range(7)), trace=False)
        self.assertEqual(len(result), 5040)
        self.assertEqual(len({tuple(row) for row in result}), 5040)
        self.assertEqual(result[0], list(range(7)))
        self.assertEqual(result[-1], list(range(6, -1, -1)))

    def test_cli(self) -> None:
        for input_data, expected in (
            ("1 2 3\n", EXAMPLE), ("0 1\n", [[0, 1], [1, 0]]),
            ("1\n", [[1]]), ("\n", [[]]), ("1 1\n", [[1, 1]]),
        ):
            result = subprocess.run(
                [sys.executable, "-m", "homework_5.permutations.solution"],
                input=input_data, cwd=Path(__file__).resolve().parents[2],
                text=True, capture_output=True, check=True, timeout=5,
            )
            lines = result.stdout.splitlines()
            with self.subTest(input_data=input_data):
                self.assertEqual(lines[0], "-> backtrack([])")
                self.assertEqual(lines[-2], "<- backtrack = None")
                self.assertEqual(ast.literal_eval(lines[-1]), expected)
                self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
