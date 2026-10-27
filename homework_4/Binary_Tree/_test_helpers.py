"""Небольшие деревья для перебора и снимки ссылок для тестов."""

from functools import cache

from .tree import Node


@cache
def tree_shapes(size: int) -> tuple:
    if size == 0:
        return (None,)
    return tuple(
        (left, right)
        for left_size in range(size)
        for left in tree_shapes(left_size)
        for right in tree_shapes(size - left_size - 1)
    )


def from_shape(shape, values) -> Node | None:
    if shape is None:
        return None
    value = next(values)
    return Node(value, from_shape(shape[0], values), from_shape(shape[1], values))


def chain(size: int, direction: str) -> Node | None:
    if size == 0:
        return None
    root = node = Node(0)
    for index in range(1, size):
        child = Node(index if direction == "right" else -index)
        setattr(node, direction, child)
        node = child
    return root


def snapshot(root: Node | None) -> dict:
    state = {}
    stack = [root]
    while stack:
        node = stack.pop()
        if node is not None and node not in state:
            state[node] = (node.value, node.left, node.right)
            stack.extend((node.left, node.right))
    return state
