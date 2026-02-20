from .binaryNode import BinaryNode


# No-rebalncing tree node
class BSTNode(BinaryNode):

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

    def subtree_insert(self, newNode:BinaryNode):
        """
        Inserts node `B` into the BST rooted at `A`, preserving BST order.
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
