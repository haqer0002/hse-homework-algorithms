"""Поиск двух разных индексов с заданной суммой."""


def two_sum(arr: list[int], k: int) -> tuple[int, int]:
    seen = {}
    for index, number in enumerate(arr):
        complement = k - number
        if complement in seen:
            return seen[complement], index
        seen[number] = index
    raise ValueError("В массиве нет пары с заданной суммой")


def main() -> None:
    arr = list(map(int, input().split()))
    k = int(input())
    print(*two_sum(arr, k))


if __name__ == "__main__":
    main()
