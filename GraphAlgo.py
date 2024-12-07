import pandas as pd
import numpy as np
def dfs(graph,frees, vertex, seq):
    seq.append(vertex)
    frees[vertex] = 0
    if vertex in graph:
        for v in graph[vertex]:
            if frees[v] == 1:
                dfs(graph, frees, v, seq)

def dfs_all_components(graph):
    frees = pd.Series(1, index=graph.keys())
    components = []
    
    for vertex in graph.keys():
        if frees[vertex] == 1:
            seq = []
            dfs(graph, frees, vertex, seq)
            components.append(seq)
    return components

import heapq

def prim(graph, start_vertex):
    mst_edges = []
    total_weight = 0
    visited = set()
    min_heap = [(0, start_vertex, None)]  # (weight, current_vertex, parent_vertex)

    while min_heap:
        weight, current_vertex, parent_vertex = heapq.heappop(min_heap)

        if current_vertex in visited:
            continue

        visited.add(current_vertex)
        if parent_vertex is not None:
            mst_edges.append((parent_vertex, current_vertex, weight))
            total_weight += weight

        for neighbor, edge_weight in graph[current_vertex]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (edge_weight, neighbor, current_vertex))

    return mst_edges, total_weight

def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])

def union(parent, rank, x, y):
    root_x = find(parent, x)
    root_y = find(parent, y)
    if rank[root_x] < rank[root_y]:
        parent[root_x] = root_y
    elif rank[root_x] > rank[root_y]:
        parent[root_y] = root_x
    else:
        parent[root_y] = root_x
        rank[root_x] += 1

def kruskal(graph: pd.DataFrame):
    """
    graph: DataFrame hoặc danh sách cạnh (edge list)
    """
    edges = []
    for i in range(graph.shape[0]):
        for j in range(i + 1, graph.shape[1]):
            if graph.iloc[i, j] != np.inf and graph.iloc[i, j] != 0:
                edges.append((i, j, graph.iloc[i, j]))

    edges = sorted(edges, key=lambda x: x[2])
    parent = [i for i in range(graph.shape[0])]
    rank = [0] * graph.shape[0]

    mst_edges = []
    total_weight = 0

    for u, v, weight in edges:
        root_u = find(parent, u)
        root_v = find(parent, v)
        if root_u != root_v:
            mst_edges.append((u, v))
            total_weight += weight
            union(parent, rank, root_u, root_v)

    return mst_edges, total_weight

def graph_coloring(graph: pd.DataFrame):
    n = graph.shape[0]
    colors = [-1] * n
    available = [True] * n

    colors[0] = 0  

    for u in range(1, n):
        for v in range(n):
            if graph.iloc[u, v] == 1 and colors[v] != -1:
                available[colors[v]] = False

        for color in range(n):
            if available[color]:
                colors[u] = color
                break

        available = [True] * n

    return colors