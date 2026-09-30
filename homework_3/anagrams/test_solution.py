"""Группы анаграмм, повторяющиеся буквы и разные символы."""

import json
import subprocess
import sys
import unittest
from collections import Counter
from itertools import product
from pathlib import Path

from .solution import group_anagrams


def canonical(groups: list[list[str]]) -> list[list[str]]:
    return sorted(sorted(group) for group in groups)


def group_by_letter_counts(words: list[str]) -> list[list[str]]:
    groups = []
    for word in words:
        for group in groups:
            if Counter(word) == Counter(group[0]):
                group.append(word)
                break
        else:
            groups.append([word])
    return groups


class AnagramsTests(unittest.TestCase):
    def test_example(self) -> None:
        words = ["eat", "tea", "tan", "ate", "nat", "bat"]
        expected = [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
        self.assertEqual(canonical(group_anagrams(words)), canonical(expected))

    def test_empty_input(self) -> None:
        self.assertEqual(group_anagrams([]), [])

    def test_single_word_and_empty_strings(self) -> None:
        self.assertEqual(group_anagrams(["abc"]), [["abc"]])
        self.assertEqual(group_anagrams(["", "", "a"]), [["", ""], ["a"]])

    def test_all_words_in_one_group(self) -> None:
        words = ["abc", "bca", "cab", "cba"]
        self.assertEqual(group_anagrams(words), [words])

    def test_no_anagrams(self) -> None:
        self.assertEqual(group_anagrams(["a", "b", "c"]), [["a"], ["b"], ["c"]])

    def test_duplicates_and_letter_multiplicity(self) -> None:
        words = ["ab", "aab", "abb", "ba", "baa", "ab"]
        self.assertEqual(group_anagrams(words), [["ab", "ba", "ab"], ["aab", "baa"], ["abb"]])

    def test_case_unicode_and_punctuation(self) -> None:
        words = ["кот", "ток", "кто", "A", "a", "åβ", "βå", "a!", "!a"]
        expected = [["кот", "ток", "кто"], ["A"], ["a"], ["åβ", "βå"], ["a!", "!a"]]
        self.assertEqual(group_anagrams(words), expected)

    def test_group_order_and_input_unchanged(self) -> None:
        words = ["tea", "bat", "eat", "tan", "nat"]
        self.assertEqual(group_anagrams(words), [["tea", "eat"], ["bat"], ["tan", "nat"]])
        self.assertEqual(words, ["tea", "bat", "eat", "tan", "nat"])

    def test_many_words_and_long_word(self) -> None:
        words = ["eat", "tea", "bat", "tab"] * 2500
        self.assertEqual(group_anagrams(words), [["eat", "tea"] * 2500, ["bat", "tab"] * 2500])
        long_word = "a" * 2000 + "b" * 2000
        self.assertEqual(group_anagrams([long_word, long_word[::-1]]), [[long_word, long_word[::-1]]])

    def test_against_letter_counts(self) -> None:
        vocabulary = ("", "a", "b", "ab", "ba", "aa", "aab", "aba")
        for size in range(4):
            for values in product(vocabulary, repeat=size):
                with self.subTest(values=values):
                    words = list(values)
                    self.assertEqual(canonical(group_anagrams(words)), canonical(group_by_letter_counts(words)))

    def test_cli(self) -> None:
        for words in (["eat", "tea", "tan", "ate", "nat", "bat"], ["", ""], ["кот", "ток"], []):
            with self.subTest(words=words):
                result = subprocess.run(
                    [sys.executable, str(Path(__file__).with_name("solution.py"))],
                    input=json.dumps(words, ensure_ascii=False) + "\n",
                    text=True, capture_output=True, check=True, timeout=5,
                )
                self.assertEqual(json.loads(result.stdout), group_by_letter_counts(words))
                self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
