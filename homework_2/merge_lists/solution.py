"""Слияние отсортированных односвязных списков перестановкой ссылок."""

from __future__ import annotations


class ListNode:
    def __init__(self, value: int, next: ListNode | None = None) -> None:
        self.value = value
        self.next = next


def merge_with_dummy(
    list1: ListNode | None, list2: ListNode | None
) -> ListNode | None:
    dummy = ListNode(0)
    tail = dummy

    while list1 is not None and list2 is not None:
        if list1.value <= list2.value:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next

    tail.next = list1 if list1 is not None else list2
    return dummy.next


def merge_without_dummy(
    list1: ListNode | None, list2: ListNode | None
) -> ListNode | None:
    if list1 is None:
        return list2
    if list2 is None:
        return list1

    if list1.value <= list2.value:
        head = list1
        list1 = list1.next
    else:
        head = list2
        list2 = list2.next
    tail = head

    while list1 is not None and list2 is not None:
        if list1.value <= list2.value:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next

    tail.next = list1 if list1 is not None else list2
    return head


def build_list(values: list[int]) -> ListNode | None:
    head = None
    for value in reversed(values):
        head = ListNode(value, head)
    return head


def to_list(head: ListNode | None) -> list[int]:
    values = []
    while head is not None:
        values.append(head.value)
        head = head.next
    return values


def main() -> None:
    list1 = build_list(list(map(int, input().split())))
    list2 = build_list(list(map(int, input().split())))
    print(*to_list(merge_with_dummy(list1, list2)))


if __name__ == "__main__":
    main()
