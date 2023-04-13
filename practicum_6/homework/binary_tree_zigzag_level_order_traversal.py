from __future__ import annotations

from collections import deque
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

        if not self.root: return []
        queue = deque([self.root])
        result, direction = [], 1

        while queue:
            level = []
            for i in range(len(queue)):
                node = queue.popleft()
                level.append(node.data)
                if node.left:  queue.append(node.left)
                if node.right: queue.append(node.right)
            result.append(level[::direction])
            direction *= (-1)
        return result


def build_tree( list_view: list[Any] ) -> BinaryTree:
    bt = BinaryTree()

    if not list_view:
        return bt

    n = len(list_view)
    root = Node(list_view[0])

    def build( node, i ):
        if i < n:
            left_idx = 2 * i + 1
            right_idx = 2 * i + 2

            if left_idx < n and list_view[left_idx] is not None:
                node.left = Node(list_view[left_idx])
                build(node.left, left_idx)

            if right_idx < n and list_view[right_idx] is not None:
                node.right = Node(list_view[right_idx])
                build(node.right, right_idx)

    build(root, 0)
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
