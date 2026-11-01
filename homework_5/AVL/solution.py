"""AVL-дерево с вставкой, удалением и поиском."""

from __future__ import annotations


class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None
        self.height = 1


def _height(node: Node | None) -> int:
    return node.height if node is not None else 0


def _update_height(node: Node) -> None:
    node.height = 1 + max(_height(node.left), _height(node.right))


def _balance(node: Node | None) -> int:
    return _height(node.left) - _height(node.right) if node is not None else 0


def _rotate_left(node: Node) -> Node:
    root = node.right
    assert root is not None
    node.right = root.left
    root.left = node
    _update_height(node)
    _update_height(root)
    return root


def _rotate_right(node: Node) -> Node:
    root = node.left
    assert root is not None
    node.left = root.right
    root.right = node
    _update_height(node)
    _update_height(root)
    return root


def _rebalance(node: Node) -> Node:
    _update_height(node)
    balance = _balance(node)
    if balance > 1:
        if _balance(node.left) < 0:
            node.left = _rotate_left(node.left)
        return _rotate_right(node)
    if balance < -1:
        if _balance(node.right) > 0:
            node.right = _rotate_right(node.right)
        return _rotate_left(node)
    return node


def _insert(node: Node | None, value: int) -> Node:
    if node is None:
        return Node(value)
    if value < node.value:
        node.left = _insert(node.left, value)
    elif value > node.value:
        node.right = _insert(node.right, value)
    else:
        return node
    return _rebalance(node)


def _delete(node: Node | None, value: int) -> Node | None:
    if node is None:
        return None
    if value < node.value:
        node.left = _delete(node.left, value)
    elif value > node.value:
        node.right = _delete(node.right, value)
    else:
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        successor = node.right
        while successor.left is not None:
            successor = successor.left
        node.value = successor.value
        node.right = _delete(node.right, successor.value)
    return _rebalance(node)


class AVL:
    def __init__(self) -> None:
        self.root: Node | None = None

    def insert(self, value: int) -> None:
        self.root = _insert(self.root, value)

    def delete(self, value: int) -> None:
        self.root = _delete(self.root, value)

    def search(self, value: int) -> bool:
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def inorder(self) -> list[int]:
        result: list[int] = []
        stack: list[Node] = []
        node = self.root
        while node is not None or stack:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            result.append(node.value)
            node = node.right
        return result


def main() -> None:
    tree = AVL()
    for value in (30, 10, 40, 5, 20, 15):
        tree.insert(value)
    print("after insert:", tree.inorder(), "root:", tree.root.value)
    for value in (5, 15, 10):
        tree.delete(value)
    print("after delete:", tree.inorder(), "root:", tree.root.value)
    print("search(40):", tree.search(40))
    print("search(15):", tree.search(15))


if __name__ == "__main__":
    main()
