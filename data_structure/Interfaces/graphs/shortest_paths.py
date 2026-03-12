from .repr import full_dfs

Adj = {
    'A':[]
}

# Before any algorithm of shortes path 
# they must use this method of initializing the single source 
# 

def INITIALIZE_SINGLE_SOURCE(Adj, s):
    dist = {vtx: float('inf') for vtx in Adj}
    parent = {vtx:None for vtx in Adj}
    
    dist[s] = 0
    
    return dist, parent
    
# We are maintaing the shortest path estimate in `dist` dictionary
# This technique of maintaing that is called Relaxationin theory
# Every algorithm also uses this for shortest path in Single Source Shortest Paths Algorithms (SSSP)
# 
def TRY_REALXING(u, v, weight, dist, parent):
    if dist[v] > dist[u] + weight:
        dist[v] = dist[u] + weight
        parent[v] = u 
 
 
 
############################################################################################################################################
#############################                        DAG-Relaxation Algorithm         ######################################################
# 
# 
# 
# 
# DAG: Directed Acyclic Graph
#   -- Special type of Directed graphs
#   -- No cycles are guranteed here 
# 
# Applications:
#   -- Compiler Design where syntax is broken into DAG
#   -- Data Pipelines 
#   -- Version Control: Git uses for track changes
#   -- Blockchain is based on DAG
#   -- for example: Apache Spark uses it
# 
# 
# 
# Explanation for the Algorithm:
# 
# Here, we have to realx the edges of its vertices
# in topological order
# that's it
# Runs in O(|V| + |E|)
def DAG_RELAXATION(graph, src):
    # get the topological order first, hmmm....,
    # Idea! Use DFS for graph traversal to give out the topological order
    _ , topo_order = full_dfs(graph)
    dist, parent = INITIALIZE_SINGLE_SOURCE(graph, src)
    # for every vertex taken in topological order
    for u in topo_order[::-1]:
        for v, weight in graph[u]:
            TRY_REALXING(u, v, weight, dist, parent)
