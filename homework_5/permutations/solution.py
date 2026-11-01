"""Перестановки методом перебора с возвратом и трассировкой вызовов."""

from homework_5.tracer.solution import tracer


def permutations(nums: list[int], trace: bool = True) -> list[list[int]]:
    remaining: dict[int, int] = {}
    for value in nums:
        remaining[value] = remaining.get(value, 0) + 1
    result: list[list[int]] = []

    def backtrack(path: list[int]) -> None:
        if len(path) == len(nums):
            result.append(path.copy())
            return
        for value in remaining:
            if remaining[value] == 0:
                continue
            remaining[value] -= 1
            path.append(value)
            backtrack(path)
            path.pop()
            remaining[value] += 1

    if trace:
        backtrack = tracer(backtrack)
    backtrack([])
    return result


def main() -> None:
    nums = [int(value) for value in input().split()]
    print(permutations(nums))


if __name__ == "__main__":
    main()
