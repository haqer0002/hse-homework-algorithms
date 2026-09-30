"""Группировка слов по буквам с сохранением повторов."""

import json


def group_anagrams(words: list[str]) -> list[list[str]]:
    groups = {}
    for word in words:
        signature = "".join(sorted(word))
        if signature not in groups:
            groups[signature] = []
        groups[signature].append(word)
    return list(groups.values())


def main() -> None:
    words = json.loads(input())
    print(json.dumps(group_anagrams(words), ensure_ascii=False))


if __name__ == "__main__":
    main()
