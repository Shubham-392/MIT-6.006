from .AVLNode import AVLNode

class AVLTree:
    def __init__(self, nodeType = AVLNode):
        self.root = None
        self.nodeType = nodeType
        self.size = 0

    def __len__(self): return self.size

    def __iter__(self):
        if self.root:
            for node in self.root.subtree_iter():
                yield node.item

        