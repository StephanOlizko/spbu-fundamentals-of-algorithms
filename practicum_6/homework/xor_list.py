from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import ctypes

import yaml


@dataclass
class Element:
    key: Any = None
    #data: Any = None
    np: int = None

    def next( self, predecessor ) -> Element:
        return ctypes.cast(id(predecessor) ^ self.np, ctypes.py_object).value

    def prev( self, successor ) -> Element:
        return ctypes.cast(id(successor) ^ self.np, ctypes.py_object).value


class XorDoublyLinkedList:
    def __init__( self ) -> None:
        self.head: Element = None
        self.tail: Element = None


    def __repr__( self ) -> str:
        return str(self)

    def __str__( self ) -> str:
        node_keys = []

        t_el = self.head
        predecessor = self.tail
        successor = t_el.next(predecessor)
        while successor != self.head:
            node_keys.append(str(t_el.key))
            predecessor = t_el
            t_el = successor
            successor = t_el.next(predecessor)

        return " <-> ".join(node_keys)

    def to_pylist( self ) -> list[Any]:
        py_list = []

        if self.empty():
            return py_list
        else:
            predecessor = self.tail
            t_el = self.head
            py_list.append(t_el.key)

            while t_el != self.tail:
                t_el = t_el.next(predecessor)
                predecessor = t_el
                py_list.append(t_el.key)

        return py_list

    def empty( self ):
        return self.head is None

    def search( self, key: Any) -> Element:
        """Complexity: O(n)"""

        pass

    def insert( self, x: Any ) -> None:
        """Insert to the front of the list (i.e., it is 'prepend')
        Complexity: O(1)
        """

        elem = Element(key=x)

        if not self.empty():
            elem.np = id(self.tail) ^ id(self.head)

            self.head.np = id(elem) ^ self.head.np
            self.tail.np = id(elem) ^ self.tail.np
            self.head = elem

        else:
            elem.np = id(elem) ^ id(elem)
            self.head = elem
            self.tail = elem


    def remove( self, x: Any ) -> None:
        """Remove x from the list
        Complexity: O(1)
        Note: My complexity is O(n), don`t know how to reduce it to O(1)
        """

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def reverse( self ) -> XorDoublyLinkedList:
        """Returns the same list but in the reserved order
        Complexity: O(1)
        """

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

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
        if i == 1:
            break

        l = XorDoublyLinkedList()
        for el in reversed(c["input"]["list"]):
            l.insert(el)
            print(el, l.to_pylist())
        for op_info in c["input"]["ops"]:
            if op_info["op"] == "insert":
                l.remove(op_info["key"])
            elif op_info["op"] == "remove":
                l.remove(op_info["key"])
            elif op_info["op"] == "reverse":
                l = l.reverse()
        py_list = l.to_pylist()
        print(f"Case #{i + 1}: {py_list == c['output']}")
        print(f"Case #{i + 1}: {py_list} {c['output']}")
