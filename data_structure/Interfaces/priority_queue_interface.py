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
    heap.build(A)           # transforms iterable A into a heap, in-place, in linear time O(n); n is the number or elements in A
    heap.insert(x)          # pushes a new item on the heap maintaing the heap property and complete binary property
    heap.delete_max()       # pops the largest item from the heap which is bascially root
"""

#####################################################################################################################
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  Base Priority Queue Interface Class  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#####################################################################################################################

from typing import Iterable


class PriorityQueueInterface:
    """
    Base interface class of a priority queue, maintains an internal array A of items, and trivially
        implements insert(x) and delete_max()
       
     (the latter being incorrect on its own, but useful for subclasses).
     
    This is Dynamic Implementation and uses O(n) extra space.
    We have implemented `PriorityQueue` In-Place class which is memory-efficient.
    """
    def __init__(self):
        self.A  =  []
        
    def insert(self, x):
        self.A.append(x)
        
    def delete_max(self):
        if len(self.A) < 1 :
            raise IndexError("Priority queue is empty")
        return self.A.pop()  # NOT CORRECT ON ITS OWN
        
    # all subclasses must implement this method
    def get_max(self):
        ...
    
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
        out.reverse()
        
        return out 
        
#####################################################################################################################
##########################       In-Place PriorityQueue (memory efficient)            ###############################

class PriorityQueue_ME:
    def __init__(self, A):
        self.n, self.A = 0, A
        
    def insert(self):      # absorb element A[n] into the queue
        if not self.n < len(self.A):
            raise IndexError("insert into full priority queue")
            
        self.n += 1
    def delete_max(self):
        if self.n < 1:
            raise IndexError("pop from empty queue")
        self.n -= 1 # NOT CORRECT ON ITS OWN 
        
    def get_max(self):
        ...
        
    @classmethod
    def sort(Queue, A):
        pq = Queue(A)               # make empty priority queue
        for i in range(len(A)):     # n x T_insert
            pq.insert()
            
        for i in range(len(A)):     # n x T_delete_max
            pq.delete_max()
            
        return pq.A
        


#####################################################################################################################
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$   Array Heaps     $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#####################################################################################################################

class PQ_Array(PriorityQueueInterface):
    
    def get_max(self):
        if len(self.A) < 1:
            raise IndexError("Priority queue is empty")
        m = 0
        for i in range(1, len(self.A)):
            if self.A[i].key > self.A[m].key:
                m = i
        return self.A[m]
    
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
        
    def get_max(self):
        if len(self.A) < 1:
            raise IndexError("Priority queue is empty")
        return self.A[-1]

#####################################################################################################################
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  Binary Heaps $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$        
#####################################################################################################################

class PQ_BinaryHeap(PriorityQueueInterface):
    def build(X:Iterable):
        n = len(X)
        for i in range(n//2, -1, -1):       # O(n) loop backward over array
            max_heapify_down(X, n, i)   # O(log n - log i)) fix max heap
    
    def insert(self, *args): # O(log n)
        super().insert(*args)
        n, A = len(self.A), self.A
        
        max_heapify_up(A, n, n-1)
        
    def get_max(self):
        if len(self.A) < 1:
            raise IndexError("Priority queue is empty")
        return self.A[0]  # max heap property guarantees max is at root
        
    def delete_max(self): # O(log n)
        n, A = len(self.A), self.A
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
        


################################################################################################################################################
# In-Place Binary Heap ############################


class PQ_BinaryHeapInPlace(PriorityQueue_ME):
    
    def build(self, up_to:int):
        self.n = up_to
        n = self.n
        for i in range(n//2, -1, -1):       # O(n) loop backward over array
            max_heapify_down(self.A, self.n, i)   # O(log n - log i)) fix max heap
    
    def insert(self): # O(log n)
        super().insert()
        n, A = self.n, self.A
        
        max_heapify_up(A, n, n-1)
        
    def delete_max(self):
        n, A = self.n - 1, self.A
        A[0], A[n] = A[n], A[0]
        
        max_heapify_down(A, n, 0)
        return super().delete_max()
        
    def get_max(self):
        if len(self.A) < 1:
            raise IndexError("Priority queue is empty")
        return self.A[0]  # max heap property guarantees max is at root
        
    def print_heap(self):
        import math
        if not self.A:
            print("Empty Heap")
            return
    
        n = self.n
        height = math.floor(math.log2(n)) + 1
        width = 2**(height) * 3  # Basic spacing
    
        print("\n--- Heap Visualization ---")
        i = 0
        for level in range(height):
            items_in_level = 2**level
            line = ""
            # Calculate leading space for this level
            spacer = " " * (width // (items_in_level + 1))
            
            for _ in range(items_in_level):
                if i < n:
                    line += f"{spacer}{A[i].key}"
                    i += 1
            print(line)
        print("--------------------------\n")
        
        
################################################################################################################    
# Example Working Code for        
# class TaskInformr:
#     def __init__(self, key, value):
#         self.key = key
#         self.value = value
        
#     def __repr__(self):
#         return f"{self.key}"
        
# A = [
#     TaskInformr(7, "task_1"), 
#     TaskInformr(3, "task_2"),
#     TaskInformr(5, "task_3"), 
#     TaskInformr(6, "task_4"),
#     TaskInformr(2, "task_5"),
#     TaskInformr(0, "task_6"),
#     TaskInformr(3, "task_7"),
#     TaskInformr(1, "task_8"),
#     TaskInformr(9, "task_9"),
#     TaskInformr(4, "task_10")
# ]

# heap = PQ_BinaryHeapInPlace(A)
# heap.build(up_to = 8)
# heap.insert()
# heap.insert()
# heap.delete_max()
# heap.delete_max()
# print(heap.get_max())
# heap.delete_max()
# print(heap.get_max())
# heap.print_heap()

# print(heap.A[:8])