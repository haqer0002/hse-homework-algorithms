"""Вложенность, аргументы, результаты и восстановление глубины после ошибок."""

from contextlib import redirect_stdout
from io import StringIO
import inspect
from pathlib import Path
import subprocess
import sys
import unittest

from .solution import factorial, tracer


FACTORIAL_TRACE = (
    "-> factorial(4)\n"
    "  -> factorial(3)\n"
    "    -> factorial(2)\n"
    "      -> factorial(1)\n"
    "      <- factorial = 1\n"
    "    <- factorial = 2\n"
    "  <- factorial = 6\n"
    "<- factorial = 24\n"
)


def capture(function, *args, **kwargs):
    output = StringIO()
    with redirect_stdout(output):
        result = function(*args, **kwargs)
    return result, output.getvalue()


class TracerTests(unittest.TestCase):
    def test_factorial_diagram(self) -> None:
        result, output = capture(factorial, 4)
        self.assertEqual(result, 24)
        self.assertEqual(output, FACTORIAL_TRACE)

    def test_base_case(self) -> None:
        result, output = capture(factorial, 0)
        self.assertEqual(result, 1)
        self.assertEqual(output, "-> factorial(0)\n<- factorial = 1\n")

    def test_positional_and_keyword_arguments(self) -> None:
        @tracer
        def greet(name, *, count=1):
            return name * count

        result, output = capture(greet, "ab", count=2)
        self.assertEqual(result, "abab")
        self.assertEqual(output, "-> greet('ab', count=2)\n<- greet = 'abab'\n")

    def test_no_arguments_and_none_result(self) -> None:
        @tracer
        def empty():
            return None

        result, output = capture(empty)
        self.assertIsNone(result)
        self.assertEqual(output, "-> empty()\n<- empty = None\n")

    def test_returned_object_is_not_copied(self) -> None:
        value = [1, 2]

        @tracer
        def identity(argument):
            return argument

        result, output = capture(identity, value)
        self.assertIs(result, value)
        self.assertEqual(value, [1, 2])
        self.assertEqual(output, "-> identity([1, 2])\n<- identity = [1, 2]\n")

    def test_metadata_and_signature(self) -> None:
        def example(value: int, *, scale: int = 2) -> int:
            """Умножить значение."""
            return value * scale

        decorated = tracer(example)
        self.assertEqual(decorated.__name__, example.__name__)
        self.assertEqual(decorated.__doc__, example.__doc__)
        self.assertEqual(inspect.signature(decorated), inspect.signature(example))
        self.assertIs(decorated.__wrapped__, example)

    def test_branching_recursion(self) -> None:
        @tracer
        def fib(n):
            return n if n < 2 else fib(n - 1) + fib(n - 2)

        result, output = capture(fib, 3)
        self.assertEqual(result, 2)
        self.assertEqual(output, (
            "-> fib(3)\n"
            "  -> fib(2)\n"
            "    -> fib(1)\n"
            "    <- fib = 1\n"
            "    -> fib(0)\n"
            "    <- fib = 0\n"
            "  <- fib = 1\n"
            "  -> fib(1)\n"
            "  <- fib = 1\n"
            "<- fib = 2\n"
        ))

    def test_mutual_recursion(self) -> None:
        @tracer
        def even(n):
            return True if n == 0 else odd(n - 1)

        @tracer
        def odd(n):
            return False if n == 0 else even(n - 1)

        result, output = capture(even, 3)
        self.assertIs(result, False)
        self.assertEqual(output, (
            "-> even(3)\n  -> odd(2)\n    -> even(1)\n      -> odd(0)\n"
            "      <- odd = False\n    <- even = False\n"
            "  <- odd = False\n<- even = False\n"
        ))

    def test_exception_is_propagated_and_depth_restored(self) -> None:
        error = ValueError("stop")

        @tracer
        def descend(n):
            if n:
                return descend(n - 1)
            raise error

        output = StringIO()
        with redirect_stdout(output):
            with self.assertRaises(ValueError) as raised:
                descend(2)
            factorial(1)
        self.assertIs(raised.exception, error)
        self.assertEqual(output.getvalue(), (
            "-> descend(2)\n  -> descend(1)\n    -> descend(0)\n"
            "    !! descend raised ValueError('stop')\n"
            "  !! descend raised ValueError('stop')\n"
            "!! descend raised ValueError('stop')\n"
            "-> factorial(1)\n<- factorial = 1\n"
        ))

    def test_caught_exception_preserves_outer_depth(self) -> None:
        @tracer
        def child():
            raise ValueError("stop")

        @tracer
        def parent():
            try:
                child()
            except ValueError:
                return 7

        result, output = capture(parent)
        self.assertEqual(result, 7)
        self.assertEqual(output, (
            "-> parent()\n  -> child()\n"
            "  !! child raised ValueError('stop')\n<- parent = 7\n"
        ))

    def test_separate_calls_start_at_zero(self) -> None:
        _, first = capture(factorial, 2)
        _, second = capture(factorial, 2)
        self.assertEqual(first, second)
        self.assertTrue(first.startswith("-> factorial(2)\n"))

    def test_permutations_share_depth_with_other_decorated_functions(self) -> None:
        from homework_5.permutations.solution import permutations

        @tracer
        def parent():
            return permutations([1, 2]), factorial(2)

        result, output = capture(parent)
        self.assertEqual(result, ([[1, 2], [2, 1]], 2))
        self.assertEqual(output, (
            "-> parent()\n"
            "  -> backtrack([])\n"
            "    -> backtrack([1])\n"
            "      -> backtrack([1, 2])\n"
            "      <- backtrack = None\n"
            "    <- backtrack = None\n"
            "    -> backtrack([2])\n"
            "      -> backtrack([2, 1])\n"
            "      <- backtrack = None\n"
            "    <- backtrack = None\n"
            "  <- backtrack = None\n"
            "  -> factorial(2)\n"
            "    -> factorial(1)\n"
            "    <- factorial = 1\n"
            "  <- factorial = 2\n"
            "<- parent = ([[1, 2], [2, 1]], 2)\n"
        ))
        self.assertEqual(capture(factorial, 1)[1], "-> factorial(1)\n<- factorial = 1\n")

    def test_negative_factorial(self) -> None:
        with redirect_stdout(StringIO()):
            with self.assertRaises(ValueError):
                factorial(-1)
        self.assertEqual(capture(factorial, 1)[1], "-> factorial(1)\n<- factorial = 1\n")

    def test_cli(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "homework_5.tracer.solution"],
            cwd=Path(__file__).resolve().parents[2],
            text=True, capture_output=True, check=True, timeout=5,
        )
        self.assertEqual(result.stdout, FACTORIAL_TRACE + "result: 24\n")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
