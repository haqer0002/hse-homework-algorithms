"""Проверка последовательностей добавления и извлечения из стека."""


def validate_stack_sequences(pushed: list[int], popped: list[int]) -> bool:
    if len(pushed) != len(popped):
        return False

    stack = []
    pop_index = 0
    for number in pushed:
        stack.append(number)
        while stack and pop_index < len(popped) and stack[-1] == popped[pop_index]:
            stack.pop()
            pop_index += 1

    return pop_index == len(popped)


def main() -> None:
    pushed = list(map(int, input().split()))
    popped = list(map(int, input().split()))
    print(validate_stack_sequences(pushed, popped))


if __name__ == "__main__":
    main()
