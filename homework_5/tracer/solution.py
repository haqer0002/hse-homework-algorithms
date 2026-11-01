"""Декоратор для вывода вложенных вызовов и результатов."""

from functools import wraps


_depth = 0


def _call(function, args, kwargs) -> str:
    arguments = [repr(value) for value in args]
    arguments.extend(f"{key}={value!r}" for key, value in kwargs.items())
    return f"{function.__name__}({', '.join(arguments)})"


def tracer(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        global _depth
        depth = _depth
        print(f"{'  ' * depth}-> {_call(function, args, kwargs)}")
        _depth += 1
        try:
            result = function(*args, **kwargs)
        except BaseException as error:
            print(f"{'  ' * depth}!! {function.__name__} raised {error!r}")
            raise
        else:
            print(f"{'  ' * depth}<- {function.__name__} = {result!r}")
            return result
        finally:
            _depth -= 1

    return wrapper


@tracer
def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return 1
    return n * factorial(n - 1)


def main() -> None:
    print("result:", factorial(4))


if __name__ == "__main__":
    main()
