"""
We must know about `Complete Binary Tree` which have following specifications:
    - type of binary tree in which every level,
      except possibly the last, is fully filled, and all nodes are as far left as possible.
      
    - This structure ensures efficient use of space 
      and allows for easy implementation of data structures like heaps.

Array as a Complete Binary Tree:
    - Idea:  interpret an array as a complete binary tree, 
             with maximum 2i nodes at depth i except
             at the largest depth, where all nodes are left-aligned
             
    - Example: 
        d_0                              _A_
        d_1                      _B_             _C_
        d_2                _D_       _E_     _F_     _G_
        d_3             _H_   _I_ _J_
        
    - Bijection between arrays and complete binary trees
        With above example equivalent array will be:
            [A, B, C, D, E, F, G, H, I, J]
            
    Compute Neighbour by index airthematic:
            left(i):   2*i + 1
            right(i):  2*i + 2
            parent(i): (i -1) // 2 ; # floor division
            
# Binary Heap -------------
    Heaps are arrays for which a[k] >= a[2*k+1] and a[k] >= a[2*k+2] for
    all k, counting elements from 0.  For the sake of comparison,
    non-existing elements are considered to be infinite.  The interesting
    property of a heap is that a[0] is always its largest element.

Max-Heap Property at node i : Q[i] ≥ Q[j] for j ∈ {left(i), right(i)}
This type of Heap is basically called as Max-Heap which obeys the above property.

In particular, max item is at root of max-heap.

USAGE:
    heap = PQ_BinaryHeap()  # initialize an empty heap from array representing complete binary tree
    heap.build(A)           # transforms iterable into a heap, in-place, in linear time O(n); n is the number or elements in A
    heap.insert(x)          # pushes a new item on the heap maintaing the heap property and complete binary property
    heap.delete_max()       # pops the largest item from the heap which is bascially root
"""

#####################################################################################################################
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  Base Priority Queue Interface Class  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#####################################################################################################################

class PriorityQueueInterface:
    """
    Base interface class of a priority queue, maintains an internal array A of items, and trivially
        implements insert(x) and delete_max()
       
     (the latter being incorrect on its own, but useful for subclasses).
    """
    def __init__(self):
        self.A  =  []
        
    def insert(self, x):
        self.A.append(x)
        
    def delete_max(self):
        if len(self.A) < 1 :
            raise IndexError("Priority queue is empty")
        return self.A.pop()  # NOT CORRECT ON ITS OWN
    
    # utility function for the class 
    @classmethod
    def sort(Queue, A):
        """
        Shared across all implementations is a method for sorting, given implementations of insert and
        delete_max. 
        
        Sorting simply makes two loops over the array: one to insert all the elements, and
        another to populate the output array with successive maxima in reverse order
        """
        pq = Queue() #make empty priority queue
        for x in A:      # n*T_insert
            pq.insert(x)
        
        out = [pq.delete_max() for _ in A] # n*T_delete_max
        out .reverse()
        
        return out 
        
#####################################################################################################################
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$   Array Heaps     $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
####################################################################################################################

class PQ_Array(PriorityQueueInterface):
    # PriortyQueueInterface.insert(x) method is already correct due to self.A =[]
    def delete_max(self):
        n, A, m = len(self.A), self.A, 0
        # get the maximum element from the array and
        # swap to the last item and then delete from the last
        for i in range(1,n):
            if A[m].key < A[i].key:
                m = i
        
        A[m], A[n] = A[n], A[m]  # swapping to the last of the Array
        
        return super().delete_max() # pop from the end of the PQ_Array
        
        
        
####################################################################################################################
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  Sorted Array Heaps $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$        
####################################################################################################################
class PQ_SortedArray(PriorityQueueInterface):
    
    # self.A is sorted so inserting will make the order change means unsort 
    # so, we have to sort the order after insertion
    # 
    def insert(self, *args):  # O(n)
        """
        We use *args to allow insert to take one argument (as makes sense now) or zero arguments;
        we will need the latter functionality when making the priority queues in-place.
        """
        super().insert(*args)   
        
        i, A = len(self.A) - 1, self.A # restore array ordering
        # bascially, it is insertion sort 
        while 0 < i and A[i + 1].key < A[i].key:
            A[i + 1], A[i] = A[i], A[i + 1]
            i -= 1
        

#####################################################################################################################
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  Binary Heaps $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$        
#####################################################################################################################

class PQ_BinaryHeap(PriorityQueueInterface):
    def insert(self, *args): # O(log n)
        super().insert(*args)
        n, A = self.n, self.A
        
        max_heapify_up(A, n, n-1)
        
    def delete_max(self): # O(log n)
        n, A = self.n, self.A
        A[0], A[n] = A[n], A[0]
        max_heapify_down(A, n, 0)
        
        return super().delete_max() # pop from the end of the array
        
def parent(i):
    p = (i-1) // 2
    return p if 0 < i else i
    
def left(i, n):
    left = (2*i) + 1
    return left if left < n else i
    
def right(i, n):
    r = (2 * i) + 2
    return r if r < n else i
    
# Here is the meat of the work done by a max heap. 
# Assuming all nodes in A[:n] satisfy the
# Max-Heap Property except for node A[i] makes it easy for these functions to maintain the Node
# Max-Heap Property locally.


def max_heapify_up(A, n, c):  # T(c) = O(log c)
    p = parent(c)              # O(1) index of parent (or c)
    if A[p].key < A[c].key:           # O(1) compare
        A[c], A[p] = A[p], A[c]       # O(1) swap parent
        max_heapify_up(A, n, p)     # T(p) = T(c/2) recursive call on parent
        
def max_heapify_down(A, n, p):                        # T(p) = O(log n - log p)
    left_item, r = left(p, n), right(p, n)                # O(1) indices of children (or p)
    c = left_item if A[r].key < A[left_item].key else r  # O(1) index of largest child
    if A[p].key < A[c].key:                                   # O(1) compare
        A[c], A[p] = A[p], A[c]                               # O(1) swap child
        max_heapify_down(A, n, c)                           # T(c) recursive call on child
        

####################################################################################################################################################
