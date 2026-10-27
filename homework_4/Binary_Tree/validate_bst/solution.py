"""Проверка строгого порядка BST с границами от всех предков."""

from homework_4.Binary_Tree.tree import Node


def is_valid_bst(root: Node | None) -> bool:
    if root is None:
        return True

    stack: list[tuple[Node, int | None, int | None]] = [(root, None, None)]
    while stack:
        node, lower, upper = stack.pop()
        if lower is not None and node.value <= lower:
            return False
        if upper is not None and node.value >= upper:
            return False

        if node.right is not None:
            stack.append((node.right, node.value, upper))
        if node.left is not None:
            stack.append((node.left, lower, node.value))
    return True


def main() -> None:
    root = Node(10, Node(5, Node(2), Node(12)), Node(15, Node(11), Node(20)))
    print(is_valid_bst(root))
    root.left.right.value = 7
    print(is_valid_bst(root))


if __name__ == "__main__":
    main()
