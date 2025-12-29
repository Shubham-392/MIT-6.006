
from typing import Iterable
from .node.BSTNode import BSTNode
from .binaryTree import BinaryTree

class BSTree(BinaryTree):
    def __init__(self):
        super().__init__(nodeType=BSTNode)

    def iter_order(self):
        yield from self

    def build(self, X:Iterable):
        for x in X:
            self.insert(x)

    def find_min(self):
        if self.root:
            return self.root.subtree_first().item

    def find_max(self):
        if self.root:
            return self.root.subtree_last().item

    def find(self, k):
        if self.root:
            node =  self.root.subtree_find(k)
            if node:
                return node.item

    def find_next(self, k):
        if self.root:
            node = self.root.subtree_find_next(k)
            if node:
                return node.item

    def find_prev(self, k):
        if self.root:
            node = self.root.subtree_find_prev(k)
            if node:
                return node.item

    def insert(self, x):

        newNode = self.nodeType(x)
        if self.root:
            self.root.subtree_insert(newNode)
            if newNode.parent is None:
                return False

        else:
            self.root = newNode
        self.size += 1
        return True

    def delete(self, k):
        assert self.root
        node = self.root.subtree_find(k)
        assert node
        ext = node.subtree_delete()
        if ext.parent is None:
            self.root = None

        self.size -= 1
        return ext.item

    def __str__(self):
        if not self.root:
            return "BST([])"
        items = [node.item.value if hasattr(node.item, 'value') else node.item
                 for node in self.root.subtree_iter()]
        return f"BST({items})"


class KeyInt:
    def __init__(self, value, key):
        self.key = key
        self.value = value

    def __str__(self) -> str:
        return self.value

list1 = [KeyInt(3,0), KeyInt(2,1), KeyInt(24,2),KeyInt(20,3),KeyInt(18,4),KeyInt(13,5)]

binary_tree = BSTree()
binary_tree.build(list1)
print(binary_tree)
