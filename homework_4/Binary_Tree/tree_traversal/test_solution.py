"""Шесть порядков, вставка, глубокие деревья и независимые эталоны."""

import subprocess
import sys
import unittest
from itertools import permutations
from pathlib import Path

from .._test_helpers import chain, snapshot
from ..tree import Node
from .solution import (
    BinarySearchTree,
    inorder,
    postorder,
    preorder,
    reverse_inorder,
    reverse_postorder,
    reverse_preorder,
)


TRAVERSALS = (
    preorder, inorder, postorder,
    reverse_preorder, reverse_inorder, reverse_postorder,
)
DIAGRAM_VALUES = (8, 3, 10, 1, 6, 9, 14, 4, 7, 13)
DIAGRAM_ORDERS = {
    "preorder": [8, 3, 1, 6, 4, 7, 10, 9, 14, 13],
    "inorder": [1, 3, 4, 6, 7, 8, 9, 10, 13, 14],
    "postorder": [1, 4, 7, 6, 3, 9, 13, 14, 10, 8],
    "reverse_preorder": [8, 10, 14, 13, 9, 3, 6, 7, 4, 1],
    "reverse_inorder": [14, 13, 10, 9, 8, 7, 6, 4, 3, 1],
    "reverse_postorder": [13, 14, 9, 10, 7, 4, 6, 1, 3, 8],
}


def reference_insert(root: Node | None, value: int) -> Node:
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = reference_insert(root.left, value)
    elif value > root.value:
        root.right = reference_insert(root.right, value)
    return root


def encode(root: Node | None):
    if root is None:
        return None
    return root.value, encode(root.left), encode(root.right)


def reference_orders(root: Node | None) -> dict[str, list[int]]:
    if root is None:
        return {function.__name__: [] for function in TRAVERSALS}
    left = reference_orders(root.left)
    right = reference_orders(root.right)
    value = [root.value]
    return {
        "preorder": value + left["preorder"] + right["preorder"],
        "inorder": left["inorder"] + value + right["inorder"],
        "postorder": left["postorder"] + right["postorder"] + value,
        "reverse_preorder": value + right["reverse_preorder"] + left["reverse_preorder"],
        "reverse_inorder": right["reverse_inorder"] + value + left["reverse_inorder"],
        "reverse_postorder": right["reverse_postorder"] + left["reverse_postorder"] + value,
    }


class TreeTraversalTests(unittest.TestCase):
    def test_empty_tree(self) -> None:
        self.assertIsNone(BinarySearchTree().root)
        for function in TRAVERSALS:
            with self.subTest(function=function.__name__):
                self.assertEqual(function(None), [])

    def test_single_node(self) -> None:
        tree = BinarySearchTree()
        tree.insert(0)
        self.assertEqual(tree.root.value, 0)
        self.assertIsNone(tree.root.left)
        self.assertIsNone(tree.root.right)
        for function in TRAVERSALS:
            self.assertEqual(function(tree.root), [0])

    def test_insertion_path_from_diagram(self) -> None:
        tree = BinarySearchTree()
        for value in DIAGRAM_VALUES[:-1]:
            tree.insert(value)
        before = snapshot(tree.root)
        tree.insert(13)
        self.assertEqual(tree.root.right.right.left.value, 13)
        self.assertEqual(len(snapshot(tree.root)), len(before) + 1)
        for node, (value, left, right) in before.items():
            self.assertEqual(node.value, value)
            if value != 14:
                self.assertIs(node.left, left)
                self.assertIs(node.right, right)
            else:
                self.assertIs(node.right, right)

    def test_diagram_orders(self) -> None:
        tree = BinarySearchTree()
        for value in DIAGRAM_VALUES:
            tree.insert(value)
        for function in TRAVERSALS:
            with self.subTest(function=function.__name__):
                self.assertEqual(function(tree.root), DIAGRAM_ORDERS[function.__name__])

    def test_duplicates_do_not_add_nodes(self) -> None:
        tree = BinarySearchTree()
        for value in (5, 3, 8):
            tree.insert(value)
        before = snapshot(tree.root)
        for value in (5, 3, 8, 3, 5):
            tree.insert(value)
        self.assertEqual(snapshot(tree.root), before)
        self.assertEqual(inorder(tree.root), [3, 5, 8])

    def test_negative_zero_and_large_values(self) -> None:
        tree = BinarySearchTree()
        values = [0, -(10**100), 10**100, -3, 4, -1]
        for value in values:
            tree.insert(value)
        self.assertEqual(inorder(tree.root), sorted(values))
        self.assertEqual(reverse_inorder(tree.root), sorted(values, reverse=True))

    def test_arbitrary_tree_with_missing_children(self) -> None:
        root = Node(0, Node(7, None, Node(-2)), Node(-5, Node(9)))
        expected = reference_orders(root)
        for function in TRAVERSALS:
            self.assertEqual(function(root), expected[function.__name__])

    def test_repeated_values_in_arbitrary_tree_are_visited(self) -> None:
        root = Node(4, Node(4), Node(4, Node(4)))
        for function in TRAVERSALS:
            self.assertEqual(function(root), [4, 4, 4, 4])

    def test_independent_tree_instances(self) -> None:
        first, second = BinarySearchTree(), BinarySearchTree()
        first.insert(10)
        second.insert(-10)
        self.assertEqual(inorder(first.root), [10])
        self.assertEqual(inorder(second.root), [-10])

    def test_tree_unchanged_and_results_independent(self) -> None:
        root = Node(5, Node(2, None, Node(3)), Node(8))
        before = snapshot(root)
        expected = reference_orders(root)
        for function in TRAVERSALS:
            result = function(root)
            result.append(999)
            self.assertEqual(function(root), expected[function.__name__])
            self.assertEqual(snapshot(root), before)

    def test_deep_chains(self) -> None:
        size = 10_000
        for direction in ("left", "right"):
            root = chain(size, direction)
            values = [index if direction == "right" else -index for index in range(size)]
            backward = values[::-1]
            expected = {
                "preorder": values,
                "inorder": values if direction == "right" else backward,
                "postorder": backward,
                "reverse_preorder": values,
                "reverse_inorder": backward if direction == "right" else values,
                "reverse_postorder": backward,
            }
            for function in TRAVERSALS:
                with self.subTest(direction=direction, function=function.__name__):
                    self.assertEqual(function(root), expected[function.__name__])

    def test_sorted_insertions_beyond_recursion_depth(self) -> None:
        size = 2000
        for values in (range(size), range(size - 1, -1, -1)):
            tree = BinarySearchTree()
            for value in values:
                tree.insert(value)
            self.assertEqual(inorder(tree.root), list(range(size)))

    def test_all_small_insertion_orders(self) -> None:
        count = 0
        for size in range(7):
            for values in permutations(range(size)):
                tree = BinarySearchTree()
                reference = None
                for value in values:
                    tree.insert(value)
                    reference = reference_insert(reference, value)
                with self.subTest(values=values):
                    self.assertEqual(encode(tree.root), encode(reference))
                    expected = reference_orders(reference)
                    for function in TRAVERSALS:
                        self.assertEqual(function(tree.root), expected[function.__name__])
                count += 1
        self.assertEqual(count, 874)

    def test_cli(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "homework_4.Binary_Tree.tree_traversal.solution"],
            cwd=Path(__file__).resolve().parents[3],
            text=True, capture_output=True, check=True, timeout=5,
        )
        expected = "".join(f"{name}: {values}\n" for name, values in DIAGRAM_ORDERS.items())
        self.assertEqual(result.stdout, expected)
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
