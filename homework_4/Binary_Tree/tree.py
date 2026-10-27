"""Узел бинарного дерева."""

from __future__ import annotations


class Node:
    def __init__(
        self,
        value: int,
        left: Node | None = None,
        right: Node | None = None,
    ) -> None:
        self.value = value
        self.left = left
        self.right = right
