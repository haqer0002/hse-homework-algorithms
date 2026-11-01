"""Порядок BST, высоты, баланс, все повороты и сравнение со множеством."""

from itertools import permutations
from math import ceil, log2
from pathlib import Path
import random
import subprocess
import sys
import unittest

from .solution import AVL


def snapshot(tree: AVL) -> dict:
    state = {}
    stack = [tree.root]
    while stack:
        node = stack.pop()
        if node is not None and node not in state:
            state[node] = (node.value, node.height, node.left, node.right)
            stack.extend((node.left, node.right))
    return state


class AVLTests(unittest.TestCase):
    def assert_tree(self, tree: AVL, expected: set[int]) -> None:
        seen = set()

        def check(node, lower=None, upper=None):
            if node is None:
                return 0
            self.assertNotIn(node, seen, "Цикл или повторное использование узла")
            seen.add(node)
            if lower is not None:
                self.assertGreater(node.value, lower)
            if upper is not None:
                self.assertLess(node.value, upper)
            left = check(node.left, lower, node.value)
            right = check(node.right, node.value, upper)
            self.assertLessEqual(abs(left - right), 1)
            self.assertEqual(node.height, 1 + max(left, right))
            return 1 + max(left, right)

        check(tree.root)
        self.assertEqual(len(seen), len(expected))
        self.assertEqual(tree.inorder(), sorted(expected))

    def build(self, values) -> AVL:
        tree = AVL()
        for value in values:
            tree.insert(value)
        return tree

    def test_empty_tree(self) -> None:
        tree = AVL()
        self.assertFalse(tree.search(0))
        tree.delete(0)
        self.assertIsNone(tree.root)
        self.assert_tree(tree, set())

    def test_single_node(self) -> None:
        tree = self.build([0])
        self.assertTrue(tree.search(0))
        self.assertFalse(tree.search(1))
        self.assert_tree(tree, {0})
        tree.delete(0)
        self.assertIsNone(tree.root)
        self.assert_tree(tree, set())

    def test_four_insertion_rotations(self) -> None:
        for values in ((3, 2, 1), (1, 2, 3), (3, 1, 2), (1, 3, 2)):
            with self.subTest(values=values):
                tree = self.build(values)
                self.assert_tree(tree, {1, 2, 3})
                self.assertEqual(tree.root.value, 2)
                self.assertEqual(tree.root.left.value, 1)
                self.assertEqual(tree.root.right.value, 3)

    def test_rotation_preserves_middle_subtrees(self) -> None:
        values = [50, 20, 70, 10, 30, 60, 80, 25, 35, 27]
        tree = AVL()
        expected = set()
        for value in values:
            tree.insert(value)
            expected.add(value)
            self.assert_tree(tree, expected)

    def test_duplicates_are_ignored(self) -> None:
        tree = self.build([3, 1, 5])
        before = snapshot(tree)
        for value in (3, 1, 5, 3, 3):
            tree.insert(value)
        self.assertEqual(snapshot(tree), before)
        self.assert_tree(tree, {1, 3, 5})

    def test_negative_zero_and_large_values(self) -> None:
        values = [0, -(10**100), 10**100, -5, 5, -1]
        tree = self.build(values)
        self.assert_tree(tree, set(values))
        for value in values:
            self.assertTrue(tree.search(value))
            tree.delete(value)
        self.assert_tree(tree, set())

    def test_search_and_inorder_do_not_change_tree(self) -> None:
        tree = self.build(range(20))
        before = snapshot(tree)
        for value in range(-1, 21):
            self.assertEqual(tree.search(value), 0 <= value < 20)
        result = tree.inorder()
        result.append(999)
        self.assertEqual(snapshot(tree), before)
        self.assertEqual(tree.inorder(), list(range(20)))

    def test_delete_missing_value(self) -> None:
        tree = self.build([3, 1, 5, 0, 2, 4, 6])
        before = snapshot(tree)
        tree.delete(-1)
        tree.delete(7)
        self.assertEqual(snapshot(tree), before)
        self.assert_tree(tree, set(range(7)))

    def test_delete_leaf(self) -> None:
        tree = self.build([4, 2, 6, 1, 3, 5, 7])
        tree.delete(1)
        self.assert_tree(tree, {2, 3, 4, 5, 6, 7})
        self.assertFalse(tree.search(1))

    def test_delete_root_with_one_child(self) -> None:
        for values in ((5, 3), (5, 7)):
            tree = self.build(values)
            tree.delete(5)
            self.assertEqual(tree.root.value, values[1])
            self.assert_tree(tree, {values[1]})

    def test_delete_internal_node_with_one_child(self) -> None:
        for values, removed in (([20, 10, 30, 5], 10), ([20, 10, 30, 35], 30)):
            tree = self.build(values)
            tree.delete(removed)
            self.assert_tree(tree, set(values) - {removed})

    def test_delete_two_children_and_successor_with_right_child(self) -> None:
        values = [20, 10, 40, 5, 15, 30, 50, 35]
        tree = self.build(values)
        tree.delete(20)
        self.assertEqual(tree.root.value, 30)
        self.assert_tree(tree, set(values) - {20})
        tree.delete(10)
        self.assert_tree(tree, set(values) - {20, 10})

    def test_four_deletion_rotations(self) -> None:
        for values, removed, root in (
            ([3, 2, 4, 1], 4, 2),
            ([2, 1, 3, 4], 1, 3),
            ([5, 2, 6, 4], 6, 4),
            ([2, 1, 5, 3], 1, 3),
        ):
            with self.subTest(values=values, removed=removed):
                tree = self.build(values)
                tree.delete(removed)
                self.assertEqual(tree.root.value, root)
                self.assert_tree(tree, set(values) - {removed})

    def test_deletion_when_heavy_child_has_zero_balance(self) -> None:
        for values, removed, root in (
            ([4, 2, 5, 1, 3], 5, 2),
            ([2, 1, 4, 3, 5], 1, 4),
        ):
            tree = self.build(values)
            tree.delete(removed)
            self.assertEqual(tree.root.value, root)
            self.assert_tree(tree, set(values) - {removed})

    def test_diagram_example(self) -> None:
        tree = self.build([30, 10, 40, 5, 20, 15])
        self.assertEqual(tree.root.value, 20)
        self.assert_tree(tree, {5, 10, 15, 20, 30, 40})
        for value in (5, 15, 10):
            tree.delete(value)
        self.assertEqual(tree.root.value, 30)
        self.assert_tree(tree, {20, 30, 40})
        self.assertTrue(tree.search(40))
        self.assertFalse(tree.search(15))

    def test_independent_instances_and_reuse(self) -> None:
        first, second = self.build([1, 2]), self.build([-1, -2])
        first.delete(1)
        first.delete(2)
        first.insert(5)
        self.assert_tree(first, {5})
        self.assert_tree(second, {-1, -2})

    def test_all_small_insertion_orders(self) -> None:
        count = 0
        for size in range(7):
            for values in permutations(range(size)):
                tree = AVL()
                expected = set()
                for value in values:
                    tree.insert(value)
                    expected.add(value)
                    self.assert_tree(tree, expected)
                count += 1
        self.assertEqual(count, 874)

    def test_all_small_insertion_and_deletion_orders(self) -> None:
        count = 0
        for size in range(5):
            orders = list(permutations(range(size)))
            for inserted in orders:
                for deleted in orders:
                    tree = self.build(inserted)
                    expected = set(inserted)
                    for value in deleted:
                        tree.delete(value)
                        expected.remove(value)
                        self.assert_tree(tree, expected)
                    self.assertIsNone(tree.root)
                    count += 1
        self.assertEqual(count, 618)

    def test_mixed_operations_against_set(self) -> None:
        generator = random.Random(42)
        tree = AVL()
        expected = set()
        for _ in range(4000):
            value = generator.randrange(-50, 51)
            operation = generator.choice(("insert", "delete", "search"))
            if operation == "insert":
                tree.insert(value)
                expected.add(value)
            elif operation == "delete":
                tree.delete(value)
                expected.discard(value)
            else:
                self.assertEqual(tree.search(value), value in expected)
            self.assert_tree(tree, expected)

    def test_ten_thousand_sorted_values_and_deletions(self) -> None:
        size = 10_000
        for values in (range(size), range(size - 1, -1, -1)):
            tree = self.build(values)
            self.assert_tree(tree, set(range(size)))
            self.assertLessEqual(tree.root.height, 2 * ceil(log2(size + 1)))
            for value in range(size):
                self.assertTrue(tree.search(value))
            for value in range(0, size, 2):
                tree.delete(value)
            self.assert_tree(tree, set(range(1, size, 2)))
            for value in range(1, size, 2):
                tree.delete(value)
            self.assertIsNone(tree.root)

    def test_cli(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "homework_5.AVL.solution"],
            cwd=Path(__file__).resolve().parents[2],
            text=True, capture_output=True, check=True, timeout=5,
        )
        self.assertEqual(result.stdout, (
            "after insert: [5, 10, 15, 20, 30, 40] root: 20\n"
            "after delete: [20, 30, 40] root: 30\n"
            "search(40): True\nsearch(15): False\n"
        ))
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
