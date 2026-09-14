"""Максимальная чётная сумма выбранных элементов массива."""

from collections.abc import Iterable


def max_even_sum(numbers: Iterable[int]) -> int:
    """Найти максимальную чётную сумму; разрешён пустой набор с суммой 0."""
    total = 0
    min_odd: int | None = None

    for number in numbers:
        total += number
        if number % 2 != 0 and (min_odd is None or number < min_odd):
            min_odd = number

    # При нечётной общей сумме хотя бы одно нечётное число обязательно есть.
    if total % 2 != 0 and min_odd is not None:
        return total - min_odd

    return total


def main() -> None:
    numbers = map(int, input().split())
    print(max_even_sum(numbers))


if __name__ == "__main__":
    main()
