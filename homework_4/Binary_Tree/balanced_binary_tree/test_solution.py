"""Высоты каждого узла, внутренний дисбаланс и все малые формы деревьев."""

import subprocess
import sys
import unittest
from itertools import repeat
from pathlib import Path

from .._test_helpers import chain, from_shape, snapshot, tree_shapes
from ..tree import Node
from .solution import is_balanced


def reference_height(root: Node | None) -> int:
    if root is None:
        return 0
    return 1 + max(reference_height(root.left), reference_height(root.right))


def reference_balanced(root: Node | None) -> bool:
    if root is None:
        return True
    return (
        abs(reference_height(root.left) - reference_height(root.right)) <= 1
        and reference_balanced(root.left)
        and reference_balanced(root.right)
    )


class BalancedBinaryTreeTests(unittest.TestCase):
    def test_empty_tree(self) -> None:
        self.assertIs(is_balanced(None), True)

    def test_single_node(self) -> None:
        self.assertIs(is_balanced(Node(0)), True)

    def test_one_child(self) -> None:
        self.assertIs(is_balanced(Node(1, Node(2))), True)
        self.assertIs(is_balanced(Node(1, None, Node(2))), True)

    def test_height_difference_two(self) -> None:
        self.assertIs(is_balanced(Node(1, Node(2, Node(3)))), False)
        self.assertIs(is_balanced(Node(1, None, Node(2, None, Node(3)))), False)

    def test_equal_leaf_depths_are_not_required(self) -> None:
        root = Node(8, Node(4, Node(2), Node(6)), Node(12))
        self.assertIs(is_balanced(root), True)

    def test_balanced_diagram_example(self) -> None:
        root = Node(8, Node(4, Node(2, Node(1)), Node(6)), Node(12, Node(10), Node(14)))
        self.assertIs(is_balanced(root), True)
        self.assertEqual(reference_height(root), 4)

    def test_imbalance_below_root_with_equal_subtree_heights(self) -> None:
        root = Node(
            8, Node(4, Node(2, Node(1))),
            Node(12, None, Node(14, None, Node(15))),
        )
        self.assertEqual(reference_height(root.left), reference_height(root.right))
        self.assertIs(is_balanced(root), False)

    def test_imbalance_in_right_subtree(self) -> None:
        root = Node(
            8, Node(4, Node(2), Node(6, Node(7))),
            Node(12, None, Node(14, None, Node(15))),
        )
        self.assertEqual(reference_height(root.left), reference_height(root.right))
        self.assertIs(is_balanced(root), False)

    def test_values_and_bst_order_do_not_matter(self) -> None:
        self.assertIs(is_balanced(Node(1, Node(100), Node(-100))), True)
        self.assertIs(is_balanced(Node(5, Node(5), Node(5, Node(5)))), True)

    def test_deep_chains(self) -> None:
        for direction in ("left", "right"):
            self.assertIs(is_balanced(chain(10_000, direction)), False)

    def test_large_perfect_tree(self) -> None:
        root = Node(0)
        level = [root]
        for _ in range(13):
            next_level = []
            for node in level:
                node.left, node.right = Node(0), Node(0)
                next_level.extend((node.left, node.right))
            level = next_level
        self.assertIs(is_balanced(root), True)

    def test_repeated_calls_and_tree_unchanged(self) -> None:
        for root, expected in (
            (Node(0, Node(0)), True), (chain(5, "left"), False), (Node(0), True),
        ):
            before = snapshot(root)
            self.assertIs(is_balanced(root), expected)
            self.assertEqual(snapshot(root), before)

    def test_all_small_tree_shapes(self) -> None:
        count = 0
        for size in range(9):
            for shape in tree_shapes(size):
                root = from_shape(shape, repeat(0))
                with self.subTest(shape=shape):
                    self.assertIs(is_balanced(root), reference_balanced(root))
                count += 1
        self.assertEqual(count, 2056)

    def test_cli(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "homework_4.Binary_Tree.balanced_binary_tree.solution"],
            cwd=Path(__file__).resolve().parents[3],
            text=True, capture_output=True, check=True, timeout=5,
        )
        self.assertEqual(result.stdout, "True\nFalse\n")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
