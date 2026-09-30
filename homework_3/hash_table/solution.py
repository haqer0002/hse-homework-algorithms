"""Хеш-таблица со списками корзин и изменением размера."""


class HashTable:
    def __init__(self, initial_capacity: int = 8) -> None:
        if initial_capacity < 1:
            raise ValueError("Число корзин должно быть положительным")
        self._initial_capacity = initial_capacity
        self._buckets: list[list[list[object]]] = [[] for _ in range(initial_capacity)]
        self._size = 0

    @property
    def capacity(self) -> int:
        return len(self._buckets)

    def __len__(self) -> int:
        return self._size

    def _find_entry(self, key: object) -> list[object] | None:
        bucket = self._buckets[hash(key) % self.capacity]
        for entry in bucket:
            if entry[0] is key or entry[0] == key:
                return entry
        return None

    def __contains__(self, key: object) -> bool:
        return self._find_entry(key) is not None

    def insert(self, key: object, value: object) -> None:
        entry = self._find_entry(key)
        if entry is not None:
            entry[1] = value
            return

        if (self._size + 1) * 4 > self.capacity * 3:
            self._resize(self.capacity * 2)
        bucket = self._buckets[hash(key) % self.capacity]
        bucket.append([key, value])
        self._size += 1

    def search(self, key: object) -> object:
        entry = self._find_entry(key)
        if entry is None:
            raise KeyError(key)
        return entry[1]

    def delete(self, key: object) -> None:
        bucket = self._buckets[hash(key) % self.capacity]
        for index, entry in enumerate(bucket):
            if entry[0] is key or entry[0] == key:
                bucket.pop(index)
                self._size -= 1
                while self.capacity > self._initial_capacity and self._size * 4 < self.capacity:
                    self._resize(max(self._initial_capacity, self.capacity // 2))
                return
        raise KeyError(key)

    def _resize(self, capacity: int) -> None:
        old_buckets = self._buckets
        self._buckets = [[] for _ in range(capacity)]
        for bucket in old_buckets:
            for entry in bucket:
                self._buckets[hash(entry[0]) % capacity].append(entry)

    def items(self) -> list[list[object]]:
        return [[entry[0], entry[1]] for bucket in self._buckets for entry in bucket]


def main() -> None:
    table = HashTable(initial_capacity=4)
    table.insert(1, "A")
    table.insert(5, "B")
    table.insert(9, "C")
    table.insert(2, "D")
    table.insert(5, "B2")
    print("search(9):", table.search(9))
    table.delete(1)
    table.delete(9)
    table.delete(2)
    print("items:", table.items())
    print("size:", len(table), "capacity:", table.capacity)


if __name__ == "__main__":
    main()
