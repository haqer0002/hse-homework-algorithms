"""Локальные и глубокие нарушения порядка, границы и полный малый перебор."""

import subprocess
import sys
import unittest
from itertools import product
from pathlib import Path

from .._test_helpers import chain, from_shape, snapshot, tree_shapes
from ..tree import Node
from .solution import is_valid_bst


def reference_inorder(root: Node | None) -> list[int]:
    if root is None:
        return []
    return reference_inorder(root.left) + [root.value] + reference_inorder(root.right)


class ValidateBSTTests(unittest.TestCase):
    def test_empty_tree(self) -> None:
        self.assertIs(is_valid_bst(None), True)

    def test_single_node(self) -> None:
        for value in (0, -1, -(10**100), 10**100):
            self.assertIs(is_valid_bst(Node(value)), True)

    def test_valid_tree(self) -> None:
        root = Node(8, Node(3, Node(1), Node(6, Node(4), Node(7))), Node(10, Node(9)))
        self.assertIs(is_valid_bst(root), True)

    def test_one_child(self) -> None:
        self.assertIs(is_valid_bst(Node(0, Node(-1))), True)
        self.assertIs(is_valid_bst(Node(0, None, Node(1))), True)

    def test_invalid_direct_children(self) -> None:
        self.assertIs(is_valid_bst(Node(5, Node(6))), False)
        self.assertIs(is_valid_bst(Node(5, None, Node(4))), False)

    def test_ancestor_bounds_on_both_sides(self) -> None:
        self.assertIs(is_valid_bst(Node(10, Node(5, None, Node(12)))), False)
        self.assertIs(is_valid_bst(Node(10, None, Node(15, Node(8)))), False)

    def test_duplicates(self) -> None:
        for root in (
            Node(5, Node(5)), Node(5, None, Node(5)),
            Node(5, Node(3, None, Node(5))),
            Node(5, None, Node(7, Node(5))),
        ):
            self.assertIs(is_valid_bst(root), False)

    def test_no_fixed_integer_limits(self) -> None:
        bound = 10**100
        self.assertIs(is_valid_bst(Node(0, Node(-bound), Node(bound))), True)
        self.assertIs(is_valid_bst(Node(bound, Node(bound - 1), Node(bound + 1))), True)
        self.assertIs(is_valid_bst(Node(-bound, Node(-bound - 1), Node(-bound + 1))), True)

    def test_diagram_example(self) -> None:
        root = Node(10, Node(5, Node(2), Node(12)), Node(15, Node(11), Node(20)))
        self.assertIs(is_valid_bst(root), False)
        root.left.right.value = 7
        self.assertIs(is_valid_bst(root), True)

    def test_balance_is_not_required(self) -> None:
        self.assertIs(is_valid_bst(chain(10, "right")), True)
        self.assertIs(is_valid_bst(Node(1, Node(2), Node(3))), False)

    def test_deep_chains(self) -> None:
        for direction in ("left", "right"):
            root = chain(10_000, direction)
            self.assertIs(is_valid_bst(root), True)
            node = root
            while getattr(node, direction) is not None:
                node = getattr(node, direction)
            node.value = root.value
            self.assertIs(is_valid_bst(root), False)

    def test_repeated_calls_and_tree_unchanged(self) -> None:
        valid = Node(0, Node(-1), Node(1))
        invalid = Node(0, Node(1), Node(-1))
        for root, expected in ((valid, True), (invalid, False), (valid, True)):
            before = snapshot(root)
            self.assertIs(is_valid_bst(root), expected)
            self.assertEqual(snapshot(root), before)

    def test_all_small_labeled_trees(self) -> None:
        count = 0
        for size in range(5):
            for shape in tree_shapes(size):
                for values in product((-1, 0, 1), repeat=size):
                    root = from_shape(shape, iter(values))
                    order = reference_inorder(root)
                    expected = all(left < right for left, right in zip(order, order[1:]))
                    with self.subTest(shape=shape, values=values):
                        self.assertIs(is_valid_bst(root), expected)
                    count += 1
        self.assertEqual(count, 1291)

    def test_cli(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "homework_4.Binary_Tree.validate_bst.solution"],
            cwd=Path(__file__).resolve().parents[3],
            text=True, capture_output=True, check=True, timeout=5,
        )
        self.assertEqual(result.stdout, "False\nTrue\n")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
