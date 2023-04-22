from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import ctypes
import time

import yaml


@dataclass
class Element:
    key: Any = None
    data: Any = None
    np: int = None

    def next( self, predecessor_id ) -> Element:
        return ctypes.cast(predecessor_id ^ self.np, ctypes.py_object).value

    def prev( self, successor_id ) -> Element:
        return ctypes.cast(successor_id ^ self.np, ctypes.py_object).value


class XorDoublyLinkedList:
    def __init__( self ) -> None:
        self.head: Element = None
        self.tail: Element = None
        self.nodes_list: list = []  #Это костыль, использующийся для того чтобы питоновский garbage collector не удалял ноды.


    def __repr__( self ) -> str:
        return str(self)

    def __str__( self ) -> str:
        node_keys = []

        node_keys = self.to_pylist()
        return " <-> ".join(node_keys)

    def to_pylist( self ) -> list[Any]:
        py_list = []

        if self.empty():
            return py_list
        else:
            predecessor_id = 0
            t_el = self.head
            py_list.append(t_el.key)

            while t_el != self.tail:
                t_el, predecessor_id = t_el.next(predecessor_id), id(t_el)
                py_list.append(t_el.key)

        return py_list

    def empty( self ):
        return self.head is None

    def search( self, key: Any ) -> Element:
        """Complexity: O(n)"""
        if self.empty():
            return None
        else:
            predecessor_id = 0
            t_el = self.head

            while t_el != self.tail:
                if t_el.key == key:
                    return t_el
                t_el, predecessor_id = t_el.next(predecessor_id), id(t_el)

        return None

    def insert( self, x: Any, data=None ) -> None:
        """Insert to the front of the list (i.e., it is 'prepend')
        Complexity: O(1)
        """

        elem = Element(key=x)

        if not self.empty():
            elem.np = id(self.head)
            elem.data = data
            self.nodes_list.append(elem)

            self.head.np = id(elem) ^ self.head.np
            self.head = elem
        else:
            elem.np = 0
            elem.data = data
            self.head = elem
            self.tail = elem
            self.nodes_list.append(elem)

    def remove( self, x: Any ) -> None:
        """Remove x from the list
        Complexity: O(1)
        Note: My complexity is O(n), don`t know how to reduce it to O(1)
        """
        if self.empty():
            return None
        else:
            predecessor_id = 0
            t_el = self.head

            while t_el != self.tail:
                if t_el.key == x:
                    successor = t_el.next(predecessor_id)
                    predecessor = ctypes.cast(predecessor_id, ctypes.py_object).value
                    successor.np = successor.np ^ id(t_el) ^ id(predecessor)
                    predecessor.np = predecessor.np ^ id(t_el) ^ id(successor)
                    self.nodes_list.remove(t_el)
                    return None

                t_el, predecessor_id = t_el.next(predecessor_id), id(t_el)

    def reverse( self ) -> XorDoublyLinkedList:
        """Returns the same list but in the reserved order
        Complexity: O(1)
        """
        self.head, self.tail = self.tail, self.head

        return self


if __name__ == "__main__":
    # You need to implement a doubly linked list using only one pointer
    # self.np per element. In python, by pointer, we understand id(object).
    # Any object can be accessed via its id, e.g.
    # >>> import ctypes
    # >>> a = ...
    # >>> ctypes.cast(id(a), ctypes.py_object).value
    # Hint: assuming that self.next and self.prev store pointers
    # define self.np as self.np = self.next XOR self.prev

    with open("xor_list_cases.yaml", "r") as f:
        cases = yaml.safe_load(f)

    for i, c in enumerate(cases):
        l = XorDoublyLinkedList()
        for el in reversed(c["input"]["list"]):
            l.insert(el)
        for op_info in c["input"]["ops"]:
            if op_info["op"] == "insert":
                l.insert(op_info["key"])
            elif op_info["op"] == "remove":
                l.remove(op_info["key"])
            elif op_info["op"] == "reverse":
                l = l.reverse()
        py_list = l.to_pylist()
        print(f"Case #{i + 1}: {py_list == c['output']}")
        print(f"Case #{i + 1}: {py_list} {c['output']}")
