"""Коллизии, изменение размера и сравнение операций с dict."""

import random
import subprocess
import sys
import unittest
from pathlib import Path

from .solution import HashTable


class CollisionKey:
    def __init__(self, value: int) -> None:
        self.value = value

    def __hash__(self) -> int:
        return -7

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CollisionKey) and self.value == other.value


class HashTableTests(unittest.TestCase):
    def test_empty_and_missing_key(self) -> None:
        table = HashTable()
        self.assertEqual(len(table), 0)
        self.assertEqual(table.items(), [])
        self.assertNotIn("missing", table)
        with self.assertRaises(KeyError):
            table.search("missing")
        with self.assertRaises(KeyError):
            table.delete("missing")
        self.assertEqual(len(table), 0)

    def test_insert_search_delete_and_reuse(self) -> None:
        table = HashTable()
        for value in (10, 0, None):
            table.insert("key", value)
            self.assertIn("key", table)
            self.assertEqual(table.search("key"), value)
            self.assertEqual(len(table), 1)
            table.delete("key")
            self.assertNotIn("key", table)
            self.assertEqual(len(table), 0)

    def test_update_does_not_add_entry_or_grow(self) -> None:
        table = HashTable(initial_capacity=4)
        for key in (1, 2, 3):
            table.insert(key, key)
        table.insert(2, "new")
        self.assertEqual(table.search(2), "new")
        self.assertEqual(len(table), 3)
        self.assertEqual(table.capacity, 4)

    def test_integer_string_and_other_hashable_keys(self) -> None:
        table = HashTable()
        entries = [[0, "zero"], [-10, "negative"], [10**50, "large"], ["кот", "word"], [None, "none"], [(1, 2), "pair"]]
        for key, value in entries:
            table.insert(key, value)
        for key, value in entries:
            self.assertEqual(table.search(key), value)
        self.assertEqual(len(table), len(entries))

    def test_equal_keys_replace_value(self) -> None:
        table = HashTable()
        table.insert(1, "first")
        table.insert(True, "second")
        table.insert(1.0, "third")
        self.assertEqual(len(table), 1)
        self.assertEqual(table.search(1), "third")

    def test_same_non_reflexive_key(self) -> None:
        table = HashTable()
        key = float("nan")
        table.insert(key, "first")
        table.insert(key, "second")
        self.assertEqual(table.search(key), "second")
        self.assertEqual(len(table), 1)
        table.delete(key)
        self.assertEqual(len(table), 0)

    def test_collisions_and_deletion_at_different_positions(self) -> None:
        for removed in range(3):
            with self.subTest(removed=removed):
                table = HashTable(initial_capacity=8)
                for key in range(3):
                    table.insert(CollisionKey(key), key * 10)
                table.delete(CollisionKey(removed))
                self.assertNotIn(CollisionKey(removed), table)
                for key in range(3):
                    if key != removed:
                        self.assertEqual(table.search(CollisionKey(key)), key * 10)
                self.assertEqual(len(table), 2)

    def test_collision_chain_survives_resizes(self) -> None:
        table = HashTable(initial_capacity=2)
        for key in range(100):
            table.insert(CollisionKey(key), key)
        for key in range(100):
            self.assertEqual(table.search(CollisionKey(key)), key)
        table.insert(CollisionKey(50), -1)
        self.assertEqual(len(table), 100)
        self.assertEqual(table.search(CollisionKey(50)), -1)
        for key in range(100):
            table.delete(CollisionKey(key))
        self.assertEqual(table.capacity, 2)

    def test_exact_grow_and_shrink_thresholds(self) -> None:
        table = HashTable(initial_capacity=4)
        for key in (1, 5, 9):
            table.insert(key, str(key))
        self.assertEqual(table.capacity, 4)
        table.insert(2, "2")
        self.assertEqual(table.capacity, 8)
        for key in (1, 5, 9, 2):
            self.assertEqual(table.search(key), str(key))
        table.delete(1)
        table.delete(9)
        self.assertEqual(table.capacity, 8)
        table.delete(2)
        self.assertEqual(table.capacity, 4)
        self.assertEqual(table.search(5), "5")

    def test_minimum_and_non_power_of_two_capacity(self) -> None:
        for capacity in (1, 3, 5):
            with self.subTest(capacity=capacity):
                table = HashTable(initial_capacity=capacity)
                for key in range(100):
                    table.insert(key, key)
                for key in range(100):
                    self.assertEqual(table.search(key), key)
                    table.delete(key)
                self.assertEqual(table.capacity, capacity)

    def test_invalid_capacity_and_unhashable_keys(self) -> None:
        for capacity in (0, -1):
            with self.assertRaises(ValueError):
                HashTable(capacity)
        table = HashTable()
        for operation in (lambda: table.insert([], 1), lambda: table.search([]), lambda: table.delete([])):
            with self.assertRaises(TypeError):
                operation()
        self.assertEqual(len(table), 0)

    def test_storage_and_item_copies_are_lists(self) -> None:
        table = HashTable(initial_capacity=4)
        for key in range(10):
            table.insert(key, key * 10)
        self.assertIsInstance(table._buckets, list)
        for bucket in table._buckets:
            self.assertIsInstance(bucket, list)
            for entry in bucket:
                self.assertIsInstance(entry, list)
                self.assertEqual(len(entry), 2)
        items = table.items()
        items[0][1] = "changed"
        items.append([99, "extra"])
        self.assertEqual(table.search(0), 0)
        self.assertNotIn(99, table)
        self.assertEqual(len(table), 10)

    def test_independent_instances(self) -> None:
        first, second = HashTable(), HashTable()
        first.insert("key", 1)
        second.insert("key", 2)
        first.delete("key")
        self.assertEqual(second.search("key"), 2)

    def test_against_dict_with_mixed_operations(self) -> None:
        rng = random.Random(42)
        table = HashTable(initial_capacity=3)
        model = {}
        for _ in range(3000):
            key = rng.randrange(-40, 41)
            operation = rng.choice(("insert", "search", "delete"))
            if operation == "insert":
                value = rng.choice((None, 0, -5, "text", 10**30))
                table.insert(key, value)
                model[key] = value
            elif operation == "search":
                if key in model:
                    self.assertEqual(table.search(key), model[key])
                else:
                    with self.assertRaises(KeyError):
                        table.search(key)
            elif key in model:
                table.delete(key)
                del model[key]
            else:
                with self.assertRaises(KeyError):
                    table.delete(key)
            self.assertEqual(len(table), len(model))
            self.assertEqual(dict(table.items()), model)
            self.assertEqual(key in table, key in model)

    def test_many_entries(self) -> None:
        table = HashTable()
        for key in range(10_000):
            table.insert(key, -key)
        self.assertEqual(len(table), 10_000)
        for key in range(10_000):
            self.assertEqual(table.search(key), -key)
            table.delete(key)
        self.assertEqual(len(table), 0)
        self.assertEqual(table.capacity, 8)

    def test_cli(self) -> None:
        result = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("solution.py"))],
            text=True, capture_output=True, check=True, timeout=5,
        )
        self.assertEqual(result.stdout, "search(9): C\nitems: [[5, 'B2']]\nsize: 1 capacity: 4\n")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
