"""Вставка в BST и шесть обходов бинарного дерева."""

from homework_4.Binary_Tree.tree import Node


class BinarySearchTree:
    def __init__(self) -> None:
        self.root: Node | None = None

    def insert(self, value: int) -> None:
        if self.root is None:
            self.root = Node(value)
            return

        node = self.root
        while True:
            if value == node.value:
                return
            if value < node.value:
                if node.left is None:
                    node.left = Node(value)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = Node(value)
                    return
                node = node.right


def _traverse(root: Node | None, order: str) -> list[int]:
    result: list[int] = []
    if root is None:
        return result

    stack = [(root, False)]
    while stack:
        node, ready = stack.pop()
        if ready:
            result.append(node.value)
            continue

        # Стек LIFO: кладём действия в обратном порядке исполнения.
        for action in reversed(order):
            if action == "N":
                stack.append((node, True))
            elif action == "L" and node.left is not None:
                stack.append((node.left, False))
            elif action == "R" and node.right is not None:
                stack.append((node.right, False))
    return result


def preorder(root: Node | None) -> list[int]:
    return _traverse(root, "NLR")


def inorder(root: Node | None) -> list[int]:
    return _traverse(root, "LNR")


def postorder(root: Node | None) -> list[int]:
    return _traverse(root, "LRN")


def reverse_preorder(root: Node | None) -> list[int]:
    return _traverse(root, "NRL")


def reverse_inorder(root: Node | None) -> list[int]:
    return _traverse(root, "RNL")


def reverse_postorder(root: Node | None) -> list[int]:
    return _traverse(root, "RLN")


def main() -> None:
    tree = BinarySearchTree()
    for value in (8, 3, 10, 1, 6, 9, 14, 4, 7, 13):
        tree.insert(value)
    for traversal in (
        preorder, inorder, postorder,
        reverse_preorder, reverse_inorder, reverse_postorder,
    ):
        print(f"{traversal.__name__}: {traversal(tree.root)}")


if __name__ == "__main__":
    main()
