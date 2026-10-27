# Binary Tree

- [Tree Traversal](tree_traversal/README.md) – BST, вставка и шесть обходов.
- [Validate BST](validate_bst/README.md) – проверка порядка во всём дереве.
- [Balanced Binary Tree](balanced_binary_tree/README.md) – проверка баланса каждого узла.

В каждой папке: `solution.py`, `test_solution.py` и README со схемой.
Общий класс [Node](tree.py) хранит целое значение `value` и ссылки `left`, `right`.
Пустое дерево задаётся как `None`.

BST использует строгий порядок: слева все значения меньше значения узла,
справа – больше. Повторная вставка существующего значения не меняет дерево.
В произвольном дереве дубликаты нарушают BST, но не мешают проверке баланса.

Команды выполняются из корня репозитория:

```bash
python3 -m homework_4.Binary_Tree.tree_traversal.solution
python3 -m homework_4.Binary_Tree.validate_bst.solution
python3 -m homework_4.Binary_Tree.balanced_binary_tree.solution
python3 -m unittest discover -s homework_4 -t . -v
```
