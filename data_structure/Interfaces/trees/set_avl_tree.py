from data_structure.Interfaces.trees.node.AVLNode import AVLNode
from data_structure.Interfaces.trees.AVLTree import AVLTree
from typing import Iterable


class SetAVLNode(AVLNode):
    def subtree_find(self, k):
        if k < self.item.key:
            if self.left:
                return self.left.subtree_find(k)
        elif k > self.item.key:
            if self.right:
                return self.right.subtree_find(k)
        else:
            return self
        return None

    def subtree_find_next(self, k):
        """
        finds the node with the smallest key strictly greater than `k`
        """
        if k >= self.item.key:
            if self.right:
                return self.right.subtree_find_next(k)
            else:
                return None
        elif self.left:
            B = self.left.subtree_find_next(k)
            if B:
                return B
        return self

    def subtree_find_prev(self, k): # O(h)
        """
        finds the node with the smallest key strictly greater than `k`
        """
        if self.item.key >= k:
            if self.left:
                return self.left.subtree_find_prev(k)
            else:
                return None
        elif self.right:
            B = self.right.subtree_find_prev(k)
            if B:
                return B
        return self

    def subtree_insert(self, newNode:AVLNode):
        """
        Inserts a new node into the subtree rooted at this node.
        """
        if  self.item.key > newNode.item.key:
            if self.left:
                self.left.subtree_insert(newNode)
            else:
                self.subtree_insert_before(newNode)
        elif  self.item.key < newNode.item.key:
            if self.right:
                self.right.subtree_insert(newNode)
            else:
                self.subtree_insert_after(newNode)
        else:
            self.item = newNode.item


class SetAVLTree(AVLTree):
    
    def __init__(self):
        super().__init__(nodeType=SetAVLNode)
        
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