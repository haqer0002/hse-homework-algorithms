"""Проверка палиндрома с помощью арифметики, без преобразования в строку."""


def is_palindrome(number: int) -> bool:
    """Вернуть True, если неотрицательное число читается одинаково в обе стороны."""
    if number < 0:
        return False

    remaining = number
    reversed_number = 0

    while remaining > 0:
        digit = remaining % 10
        reversed_number = reversed_number * 10 + digit
        remaining //= 10

    return reversed_number == number


def main() -> None:
    number = int(input())
    print(is_palindrome(number))


if __name__ == "__main__":
    main()
