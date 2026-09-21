"""Оба способа слияния: значения, исходные узлы и отсутствие циклов."""

import subprocess
import sys
import unittest
from itertools import combinations_with_replacement
from pathlib import Path
from unittest.mock import patch

from . import solution
from .solution import ListNode, build_list, merge_with_dummy, merge_without_dummy, to_list


def collect_nodes(head: ListNode | None) -> list[ListNode]:
    nodes = []
    seen = set()
    while head is not None:
        if id(head) in seen:
            raise AssertionError("В списке обнаружен цикл")
        seen.add(id(head))
        nodes.append(head)
        head = head.next
    return nodes


class MergeListsTests(unittest.TestCase):
    def check_merge(self, left: list[int], right: list[int]) -> None:
        for merge in (merge_with_dummy, merge_without_dummy):
            with self.subTest(method=merge.__name__, left=left, right=right):
                list1, list2 = build_list(left), build_list(right)
                original_nodes = collect_nodes(list1) + collect_nodes(list2)
                original_values = [node.value for node in original_nodes]
                expected_nodes = sorted(original_nodes, key=lambda node: node.value)
                result = merge(list1, list2)
                result_nodes = collect_nodes(result)
                self.assertEqual([node.value for node in result_nodes], sorted(left + right))
                self.assertEqual(result_nodes, expected_nodes)
                self.assertEqual([node.value for node in original_nodes], original_values)

    def test_example(self) -> None:
        self.check_merge([1, 2, 4], [1, 3, 4])

    def test_empty_lists(self) -> None:
        for left, right in (([], []), ([], [1, 2]), ([1, 2], [])):
            self.check_merge(left, right)

    def test_single_elements(self) -> None:
        for left, right in (([1], [2]), ([2], [1]), ([1], [1])):
            self.check_merge(left, right)

    def test_disjoint_ranges(self) -> None:
        self.check_merge([1, 2, 3], [7, 8, 9])
        self.check_merge([7, 8, 9], [1, 2, 3])

    def test_interleaving_and_unequal_lengths(self) -> None:
        self.check_merge([1, 3, 5, 7, 9], [2, 4])
        self.check_merge([2, 4], [1, 3, 5, 7, 9])

    def test_duplicates(self) -> None:
        self.check_merge([2, 2, 2], [2, 2])
        self.check_merge([1, 1, 4, 4], [1, 2, 4, 4, 4])

    def test_negative_zero_and_large_values(self) -> None:
        self.check_merge([-10**30, -5, 0, 10**30], [-9, 0, 8, 10**30])

    def test_all_small_sorted_lists(self) -> None:
        lists = [
            list(values)
            for size in range(5)
            for values in combinations_with_replacement((-1, 0, 1), size)
        ]
        for left in lists:
            for right in lists:
                self.check_merge(left, right)

    def test_allocates_only_dummy_node(self) -> None:
        for merge, expected_count in ((merge_with_dummy, 1), (merge_without_dummy, 0)):
            with self.subTest(method=merge.__name__):
                list1, list2 = build_list([1, 3]), build_list([2, 4])
                with patch.object(solution, "ListNode", wraps=ListNode) as constructor:
                    result = merge(list1, list2)
                self.assertEqual(constructor.call_count, expected_count)
                self.assertEqual(to_list(result), [1, 2, 3, 4])

    def test_long_lists(self) -> None:
        self.check_merge(list(range(0, 10_000, 2)), list(range(1, 10_000, 2)))

    def test_conversion_helpers(self) -> None:
        self.assertIsNone(build_list([]))
        self.assertEqual(to_list(None), [])
        values = [-1, 0, 0, 8]
        self.assertEqual(to_list(build_list(values)), values)

    def test_cli(self) -> None:
        for input_data, expected in (
            ("1 2 4\n1 3 4\n", "1 1 2 3 4 4\n"),
            ("\n1 2\n", "1 2\n"),
            ("\n\n", "\n"),
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
