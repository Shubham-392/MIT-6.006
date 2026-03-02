# 
# author: Shubham <123jangrashubham@gmail.com>
# Date: 03/01/2026
# Lecture: MIT-6.006 L09 (2020)
# Implementation: BFS and shortest path with BFS
# 
# Graph Representation of labeled graphs as per MIT 6.006 (Intro to algorithms)
Adj = {}
def add_vertex(*args:str):
    for arg in args:
        Adj[arg] = []
        
def build_edge(from_v:str, to_v:str):
    if from_v in Adj and to_v in Adj:
        Adj[from_v].append(to_v)  # graph is undirected so only single edge 
    else:
        raise ValueError("Vertices not in graph")
        
def get_graph():
    return Adj
 
###############################################################################################################   
# Algorithms for Graph
# BFS, DFS, etc

def bfs(Adj, start_v:str)-> dict:                  # Adj: adjacency list, start_v: starting vertex; `O(|V|+|E|)`
    """
    returns 
        Parent labels (pointers) together determine a BFS tree from vertex s, containing some
        shortest path from s to every other vertex in the graph.
    """
    if start_v not in Adj:
       raise ValueError("starting vertex is not in graph")
    parent = {v: None for v in Adj.keys()}       #  O(V) (use DAA if labeled)
    parent[start_v] = start_v                            #  O(1) root
    
    level = [[start_v]]                 # O(1) initialize levels
    
    while 0 < len(level[-1]):
        level.append([])                                 # O(1) amortized, make new level
        for u in level[-2]:
            for v in Adj[u]:                             # O(Adj[u]) loop over neighbors
                if parent[v] is None:
                    parent[v] = u
                    level[-1].append(v)
    
    return parent 


# We can use parent labels returned by a breadth-first search to construct a shortest path from a vertex
# start_v to vertex target_v, following parent pointers from target_v backward through the graph to start_v.\
# below is the python implementation to compute 
# shortest path from vertex start_v  to  vertex target_v
# which also runs in O(|V|+|E|)

def unweighted_shortest_path(Adj, start_v, target_v):
    parent = bfs(Adj, start_v)                               # O(V + E) BFS tree from start_v
    
    if parent[target_v] is None:
        return None
        
    i = target_v            # O(1) label of current vertex
    path = [target_v]      # O(1) initialize path
    
    while i != start_v:                                          # O(V) walk back to start_V
        i = parent[i]
        path.append(i)
        
    return path[::-1]                                            # O(V) return reversed path
    
# NOTE: All vertices are labelled 
# the parent array returned has length |V |,v∈ V
# depth-first search runs in O(|V | + |E|) time.
# This function only visits the connected nodes
# Not visiting the nodes which is not directly connected to any node
# So, we need a full-method to visit the the nodes that has not been discovered by the search
# In- below implementation you will find a method of `full_dfs(Adj)`
def dfs(Adj, start_v, parent=None, order=None):      # Adj: adjacency list, s: start
    if parent is None:
        parent = {v:None for v in Adj.keys()}
        parent[start_v] = start_v
        order = []
    
    for v in Adj[start_v]:          # O(Adj[s]) loop over neighbors
        if parent[v] is None:
            parent[v] = start_v
            dfs(Adj, v, parent, order)      # Recursive call
            
    order.append(start_v)                           # O(1) amortized
    
    return parent, order
    
# Such a search is conceptually equivalent to adding an auxiliary vertex
# with an outgoing edge to every vertex in the graph and then running breadth-first or depth-first
# search from the added vertex
# Python code searching an entire graph via depth-first search is given
# below
def full_dfs(Adj):
    parent = {v:None for v in Adj.keys()}
    order = []
    
    for v in range(len(Adj)):
        if parent[v] is None:
            parent[v] = v
            dfs(Adj, v, parent, order)
            
    return parent, order
    
    
    
# Cycle-detection in a graph
# i.e., track a backedge

def cycle_detection_dfs(
    Adj, 
    start_v, 
    parent=None, 
    order=None,
    ancestors=None,
    cycles=None
):
    if parent is None:
        parent = {v:None for v in Adj.keys()}
        parent[start_v] = start_v
        order = []
        back_edges = [0]
        #initialize the ancestor set to keep track of the 
        # active nodes
        ancestors = set()
    # add very first visiting node    
    ancestors.add(start_v)
    for v in Adj[start_v]:          # O(Adj[s]) loop over neighbors
        if parent[v] is None:
            parent[v] = start_v
            cycle_detection_dfs(Adj, v, parent, order)      # Recursive call
        
        elif v in ancestors:
            # Backedge found 
            back_edges[0] += 1
            
    order.append(start_v)                           # O(1) amortized
    # When backtracking remove the ancestors as we have visited the node 
    # and no sense to keep in active list
    # So, better to remove them 
    ancestors.remove(start_v)
    return back_edges[0]
    
