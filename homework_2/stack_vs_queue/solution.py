"""Стек и очередь на односвязных списках."""

from __future__ import annotations


class _Node:
    def __init__(self, value: int, next: _Node | None = None) -> None:
        self.value = value
        self.next = next


class Stack:
    def __init__(self) -> None:
        self._top: _Node | None = None
        self._size = 0

    def push(self, value: int) -> None:
        self._top = _Node(value, self._top)
        self._size += 1

    def pop(self) -> int:
        if self._top is None:
            raise IndexError("pop from empty stack")
        value = self._top.value
        self._top = self._top.next
        self._size -= 1
        return value

    def peek(self) -> int:
        if self._top is None:
            raise IndexError("peek from empty stack")
        return self._top.value

    def is_empty(self) -> bool:
        return self._top is None

    def __len__(self) -> int:
        return self._size


class Queue:
    def __init__(self) -> None:
        self._head: _Node | None = None
        self._tail: _Node | None = None
        self._size = 0

    def enqueue(self, value: int) -> None:
        node = _Node(value)
        if self._tail is None:
            self._head = node
        else:
            self._tail.next = node
        self._tail = node
        self._size += 1

    def dequeue(self) -> int:
        if self._head is None:
            raise IndexError("dequeue from empty queue")
        value = self._head.value
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return value

    def peek(self) -> int:
        if self._head is None:
            raise IndexError("peek from empty queue")
        return self._head.value

    def is_empty(self) -> bool:
        return self._head is None

    def __len__(self) -> int:
        return self._size


def main() -> None:
    stack = Stack()
    queue = Queue()
    for value in (10, 20, 30):
        stack.push(value)
        queue.enqueue(value)
    print("Stack:", stack.pop(), stack.pop(), stack.pop())
    print("Queue:", queue.dequeue(), queue.dequeue(), queue.dequeue())


if __name__ == "__main__":
    main()
