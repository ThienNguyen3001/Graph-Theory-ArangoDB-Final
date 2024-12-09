import pandas as pd
from collections import deque
from copy import deepcopy
import numpy as np
import heapq
def dfs(graph,frees, vertex, seq):
    seq.append(vertex)
    frees[vertex] = 0
    for v in graph.get(vertex, []):
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

def has_euler_cycle(graph):
    return all(len(neighbors) % 2 == 0 for neighbors in graph.values())

def find_euler_cycle(graph):
    if not has_euler_cycle(graph):
        return None
    g = {k: list(v) for k, v in graph.items()}
    cycle, stack = [], [list(g.keys())[0]]
    while stack:
        current = stack[-1]
        if not g[current]:
            cycle.append(current)
            stack.pop()
        else:
            neighbor = g[current].pop(0)
            g[neighbor].remove(current)
            stack.append(neighbor)
    return cycle[::-1]

def has_hamilton_cycle(adjacency_list):
    vertices, n = list(adjacency_list.keys()), len(adjacency_list)
    
    def is_valid_path(path):
        # Kiểm tra tất cả các cạnh có tồn tại và chu trình đóng
        return all(path[i + 1] in adjacency_list[path[i]] for i in range(n - 1)) and path[-1] in adjacency_list[path[0]]
    
    def backtrack(path):
        if len(path) == n:  # Nếu đi qua tất cả các đỉnh
            return is_valid_path(path)
        for v in vertices:
            if v not in path:
                path.append(v)
                if backtrack(path):
                    return True
                path.pop()
        return False
    
    return backtrack([vertices[0]])

def find_hamilton_cycle(adjacency_list, start):
    def backtrack(path):
        print(f"Đường đi Backtracking : {path}")
        if len(path) == len(adjacency_list) and start in adjacency_list[path[-1]]:
            print(f"Đường đi: {path + [start]}")
            return path + [start]  # Thêm đỉnh quay về
        for next_vertex in adjacency_list[path[-1]]:
            if next_vertex not in path:
                result = backtrack(path + [next_vertex])
                if result:
                    return result
        return None

    return backtrack([start])

def find_euler_path(graph, start):
    temp_graph, path, stack = deepcopy(graph), [], [start]
    while stack:
        current = stack[-1]
        if temp_graph[current]:
            next_vertex = temp_graph[current].pop(0)
            temp_graph[next_vertex].remove(current)
            stack.append(next_vertex)
        else:
            path.append(stack.pop())
    return path[::-1]

def is_valid_hamilton_cycle(cycle, graph):
    return len(cycle) == len(graph) and len(set(cycle)) == len(graph) and all(cycle[i+1] in graph[cycle[i]] for i in range(len(cycle) - 1)) and cycle[0] in graph[cycle[-1]]

def bfs(graph, start):
    visited, queue, traversal_order = set(), deque([start]), []
    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            traversal_order.append(vertex)
            queue.extend(neighbor for neighbor in graph.get(vertex, []) if neighbor not in visited)
    return traversal_order

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

def kruskal(graph):
    edges = []
    for u in graph:
        for v, weight in graph[u]:
            edges.append((u, v, weight))

    edges = sorted(edges, key=lambda x: x[2])
    parent = {v: v for v in graph}
    rank = {v: 0 for v in graph}

    mst_edges = []
    total_weight = 0

    for u, v, weight in edges:
        root_u = find(parent, u)
        root_v = find(parent, v)
        if root_u != root_v:
            mst_edges.append((u, v, weight))
            total_weight += weight
            union(parent, rank, root_u, root_v)

    return mst_edges, total_weight

def graph_coloring(graph, colors):
    n = len(graph)  
    
    for vertex in range(1, n):
        # Track available colors
        available = [True] * n
        
        
        for neighbor in graph[vertex]:
            if colors[neighbor] != -1:
                available[colors[neighbor]] = False
        
        # Find first available color
        for color in range(n):
            if available[color]:
                colors[vertex] = color
                break
                
    return colors
