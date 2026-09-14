"""Подсчёт простых чисел с помощью решета Эратосфена."""


def count_primes(n: int) -> int:
    """Вернуть количество простых чисел, строго меньших n."""
    if n <= 2:
        return 0

    is_prime = [True] * n
    is_prime[0] = False
    is_prime[1] = False

    p = 2
    while p * p < n:
        if is_prime[p]:
            for multiple in range(p * p, n, p):
                is_prime[multiple] = False
        p += 1

    return sum(is_prime)


def main() -> None:
    n = int(input())
    print(count_primes(n))


if __name__ == "__main__":
    main()
