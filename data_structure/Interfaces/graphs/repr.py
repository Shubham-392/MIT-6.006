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
    