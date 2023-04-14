from __future__ import annotations

from queue import Queue
from dataclasses import dataclass
from typing import Any

import yaml


@dataclass
class Node:
    key: Any
    data: Any = None
    left: Node = None
    right: Node = None

    def __init__( self, data=0, left=None, right=None ):
        self.data = data
        self.left = left
        self.right = right


class BinaryTree:
    def __init__( self ) -> None:
        self.root: Node = None

    def empty( self ) -> bool:
        return self.root is None

    def zigzag_level_order_traversal( self ) -> list[Any]:

        if not self.root:
            return []

        queue = Queue()
        queue.put(self.root)

        res = []
        curr = []
        level = 0

        while not queue.empty():
            size = queue.qsize()
            curr = []
            for sz in range(size):
                temp = queue.get()
                if level % 2 == 0:
                    curr.append(temp.data)
                else:
                    curr.insert(0, temp.data)

                if temp.left:
                    queue.put(temp.left)
                if temp.right:
                    queue.put(temp.right)

            level = not level
            res.append(curr)
        return res


def build_tree( list_view: list[Any] ) -> BinaryTree:
    bt = BinaryTree()

    if not list_view:
        return bt

    root = Node(list_view[0])
    stack = [(root, 0)]

    while stack:
        node, list_iter = stack.pop()

        if 2 * list_iter + 1 < len(list_view) and list_view[2 * list_iter + 1] is not None:
            node.left = Node(list_view[2 * list_iter + 1])
            stack.append((node.left, 2 * list_iter + 1))

        if 2 * list_iter + 2 < len(list_view) and list_view[2 * list_iter + 2] is not None:
            node.right = Node(list_view[2 * list_iter + 2])
            stack.append((node.right, 2 * list_iter + 2))

    bt.root = root
    return bt


if __name__ == "__main__":
    # Let's solve Binary Tree Zigzag Level Order Traversal problem from leetcode.com:
    # https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/
    # First, implement build_tree() to read a tree from a list format to our class
    # Second, implement BinaryTree.zigzag_traversal() returning the list required by the task
    # Avoid recursive traversal!

    with open(
            "binary_tree_zigzag_level_order_traversal_cases.yaml", "r"
    ) as f:
        cases = yaml.safe_load(f)

    for i, c in enumerate(cases):
        bt = build_tree(c["input"])
        zz_traversal = bt.zigzag_level_order_traversal()
        print(f"Case #{i + 1}: {zz_traversal == c['output']}")
