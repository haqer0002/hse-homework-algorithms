"""Проверка баланса дерева через вычисление высот снизу вверх."""

from homework_4.Binary_Tree.tree import Node


def is_balanced(root: Node | None) -> bool:
    stack = [(root, False)]
    heights: list[int] = []
    while stack:
        node, ready = stack.pop()
        if node is None:
            heights.append(0)
        elif not ready:
            stack.append((node, True))
            stack.append((node.right, False))
            stack.append((node.left, False))
        else:
            # Левое поддерево завершилось первым, правое — последним.
            right_height = heights.pop()
            left_height = heights.pop()
            if abs(left_height - right_height) > 1:
                return False
            heights.append(1 + max(left_height, right_height))
    return True


def main() -> None:
    balanced = Node(
        8, Node(4, Node(2, Node(1)), Node(6)), Node(12, Node(10), Node(14)),
    )
    unbalanced = Node(
        8, Node(4, Node(2, Node(1))), Node(12, None, Node(14, None, Node(15))),
    )
    print(is_balanced(balanced))
    print(is_balanced(unbalanced))


if __name__ == "__main__":
    main()
