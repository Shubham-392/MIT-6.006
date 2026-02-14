
def height(A):
    if A :
        return A.height
    else:
        return -1

class AVLNode:
    
    def __init__(self, x):
        self.left = None
        self.right = None
        self.parent = None
        self.item = x
        self.subtree_update()
        
    def subtree_update(self):
        self.height = 1 + max(height(self.left), height(self.right))

    def skew(self):
        return height(self.right) - height(self.left)
        
    def subtree_iter(self):
        if self.left:
            yield from self.left.subtree_iter()
        yield self
        if self.right:
            yield from self.right.subtree_iter()
            
    def subtree_first(self):
        """
        – If <X> has left child, recursively return the first node in the left subtree

        – Otherwise, <X> is the first node, so return it

        Running time is O(h) where h is the height of the tree
        """
        if self.left:
            return self.left.subtree_first()
        else:
            return self

    def subtree_last(self):
        """
        return: the last node in the traversal order
            – If <X> has right child, recursively return the last node in the right subtree

            – Otherwise, <X> is the last node, so return it

        Running time is O(h) where h is the height of the tree
        """
        if self.right:
            return self.right.subtree_last()
        else:
            return self
            
    def successor(self):
        """
        In a tree to find successor:

            -- if `<X>` has right child, return first of right subtree

            -- Otherwise, return lowest ancestor of <X> for which <X> is in its left subtree

        Running time is O(h) where h is the height of the tree
        """
        # case1: if has right child
        if self.right:
            return self.right.subtree_first()

        # case2: otherwise, lowest ancestor for which node is in lowest ancestor's left subtree
        curr = self
        while (curr.parent) and (curr is curr.parent.right):
            curr = curr.parent
        # finally return
        return curr.parent

    def predecessor(self):
        """
        In a tree to find predecessor:

            -- if `<X>` has left child, return last of left subtree

            -- Otherwise, return lowest ancestor of <X> for which <X> is in its right subtree

        Running time is O(h) where h is the height of the tree
        """
        # case1: if has left child
        if self.left:
            return self.left.subtree_last()

        # case2: otherwise, lowest ancestor for which node is in lowest ancestor's right subtree
        curr = self
        while (curr.parent) and (curr is curr.parent.left):
            curr = curr.parent
        # finally return
        return curr.parent
        
    def subtree_insert_before(self, B): # O(log n)
        if self.left:
            self = self.left.subtree_last()
            self.right, B.parent = B, self
        else:
            self.left, B.parent = B, self
        self.maintain()
        
    def subtree_insert_after(self, B): # O(log n)
        if self.right:
            self = self.right.subtree_first()
            self.left, B.parent = B, self
        else:
            self.right, B.parent = B, self
        self.maintain()
        
    def subtree_delete(self): # O(log n)
        if self.left or self.right:
            if self.left:
                B = self.predecessor()
            else: 
                B = self.successor()
            self.item, B.item = B.item, self.item
            return B.subtree_delete()
        if self.parent:
            if self.parent.left is self: 
                self.parent.left = None
            else: 
                self.parent.right = None
                
            self.parent.maintain()
        return self
    
    def rebalance(self):
        if self.skew() == 2:
            if self.right.skew() < 0:
                self.right.subtree_rotate_right()
            self.subtree_rotate_left()
        elif self.skew() == -2:
            if self.left.skew() > 0:
                self.left.subtree_rotate_left()
            self.subtree_rotate_right()
            
            
    def maintain(self):
        self.rebalance()
        self.subtree_update()
        if self.parent:
            self.parent.maintain()
     
    # rotation part is looking ugly
    # will clean in another commits(if possible)
            
    def subtree_rotate_right(self): # O(1)
        assert self.left
        B, E = self.left, self.right
        A, C = B.left, B.right
        self, B = B, self
        self.item, B.item = B.item, self.item
        B.left, B.right = A, self
        self.left, self.right = C, E
        if A: 
            A.parent = B
        if E: 
            E.parent = self
        B.subtree_update()
        self.subtree_update()
        
    def subtree_rotate_left(self): # O(1)
        assert self.right
        A, D = self.left, self.right
        C, E = D.left, D.right
        self, D = D, self
        self.item, D.item = D.item, self.item
        D.left, D.right = self, E
        self.left, self.right = A, C
        if A: 
            A.parent = self
        if E:
            E.parent = D
        self.subtree_update()
        D.subtree_update()