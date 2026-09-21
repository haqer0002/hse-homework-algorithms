"""Проверка порядка, пустого состояния и чередования операций."""

import subprocess
import sys
import unittest
from itertools import product
from pathlib import Path

from .solution import Queue, Stack


class StackTests(unittest.TestCase):
    def test_empty(self) -> None:
        stack = Stack()
        self.assertTrue(stack.is_empty())
        self.assertEqual(len(stack), 0)
        with self.assertRaises(IndexError):
            stack.pop()
        with self.assertRaises(IndexError):
            stack.peek()
        self.assertEqual(len(stack), 0)

    def test_single_element_and_reuse(self) -> None:
        stack = Stack()
        for value in (0, -3, 10**30):
            stack.push(value)
            self.assertFalse(stack.is_empty())
            self.assertEqual(stack.peek(), value)
            self.assertEqual(len(stack), 1)
            self.assertEqual(stack.pop(), value)
            self.assertTrue(stack.is_empty())
            self.assertEqual(len(stack), 0)

    def test_lifo_and_duplicates(self) -> None:
        stack = Stack()
        values = [4, -1, 4, 0, 8]
        for value in values:
            stack.push(value)
        self.assertEqual([stack.pop() for _ in values], values[::-1])

    def test_peek_does_not_remove(self) -> None:
        stack = Stack()
        stack.push(10)
        stack.push(20)
        self.assertEqual(stack.peek(), 20)
        self.assertEqual(stack.peek(), 20)
        self.assertEqual(len(stack), 2)
        self.assertEqual(stack.pop(), 20)
        self.assertEqual(stack.peek(), 10)

    def test_independent_instances(self) -> None:
        first, second = Stack(), Stack()
        first.push(10)
        second.push(20)
        self.assertEqual(first.pop(), 10)
        self.assertEqual(second.pop(), 20)

    def test_large_stack(self) -> None:
        stack = Stack()
        for value in range(10_000):
            stack.push(value)
        self.assertEqual(len(stack), 10_000)
        self.assertEqual([stack.pop() for _ in range(10_000)], list(range(9999, -1, -1)))
        self.assertTrue(stack.is_empty())


class QueueTests(unittest.TestCase):
    def test_empty(self) -> None:
        queue = Queue()
        self.assertTrue(queue.is_empty())
        self.assertEqual(len(queue), 0)
        with self.assertRaises(IndexError):
            queue.dequeue()
        with self.assertRaises(IndexError):
            queue.peek()
        self.assertEqual(len(queue), 0)

    def test_single_element_and_reuse(self) -> None:
        queue = Queue()
        for value in (0, -3, 10**30):
            queue.enqueue(value)
            self.assertFalse(queue.is_empty())
            self.assertEqual(queue.peek(), value)
            self.assertEqual(len(queue), 1)
            self.assertEqual(queue.dequeue(), value)
            self.assertTrue(queue.is_empty())
            self.assertEqual(len(queue), 0)
            self.assertIsNone(queue._head)
            self.assertIsNone(queue._tail)

    def test_fifo_and_duplicates(self) -> None:
        queue = Queue()
        values = [4, -1, 4, 0, 8]
        for value in values:
            queue.enqueue(value)
        self.assertEqual([queue.dequeue() for _ in values], values)

    def test_peek_does_not_remove(self) -> None:
        queue = Queue()
        queue.enqueue(10)
        queue.enqueue(20)
        self.assertEqual(queue.peek(), 10)
        self.assertEqual(queue.peek(), 10)
        self.assertEqual(len(queue), 2)
        self.assertEqual(queue.dequeue(), 10)
        self.assertEqual(queue.peek(), 20)

    def test_independent_instances(self) -> None:
        first, second = Queue(), Queue()
        first.enqueue(10)
        second.enqueue(20)
        self.assertEqual(first.dequeue(), 10)
        self.assertEqual(second.dequeue(), 20)

    def test_large_queue(self) -> None:
        queue = Queue()
        for value in range(10_000):
            queue.enqueue(value)
        self.assertEqual(len(queue), 10_000)
        self.assertEqual([queue.dequeue() for _ in range(10_000)], list(range(10_000)))
        self.assertTrue(queue.is_empty())


class MixedOperationsTests(unittest.TestCase):
    def test_all_short_operation_patterns(self) -> None:
        for operations in product(("add", "remove"), repeat=8):
            with self.subTest(operations=operations):
                stack, queue = Stack(), Queue()
                stack_model, queue_model = [], []
                for value, operation in enumerate(operations):
                    if operation == "add":
                        stack.push(value)
                        queue.enqueue(value)
                        stack_model.append(value)
                        queue_model.append(value)
                    elif stack_model:
                        self.assertEqual(stack.pop(), stack_model.pop())
                        self.assertEqual(queue.dequeue(), queue_model.pop(0))
                    else:
                        with self.assertRaises(IndexError):
                            stack.pop()
                        with self.assertRaises(IndexError):
                            queue.dequeue()
                    self.assertEqual(len(stack), len(stack_model))
                    self.assertEqual(len(queue), len(queue_model))
                    self.assertEqual(stack.is_empty(), not stack_model)
                    self.assertEqual(queue.is_empty(), not queue_model)
                    if stack_model:
                        self.assertEqual(stack.peek(), stack_model[-1])
                        self.assertEqual(queue.peek(), queue_model[0])

    def test_diagram_example(self) -> None:
        stack, queue = Stack(), Queue()
        for value in (10, 20, 30):
            stack.push(value)
            queue.enqueue(value)
        self.assertEqual((stack.pop(), queue.dequeue()), (30, 10))
        stack.push(40)
        queue.enqueue(40)
        for expected in ((40, 20), (20, 30), (10, 40)):
            self.assertEqual((stack.pop(), queue.dequeue()), expected)
        self.assertTrue(stack.is_empty())
        self.assertTrue(queue.is_empty())

    def test_cli(self) -> None:
        result = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("solution.py"))],
            text=True, capture_output=True, check=True, timeout=5,
        )
        self.assertEqual(result.stdout, "Stack: 30 20 10\nQueue: 10 20 30\n")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
