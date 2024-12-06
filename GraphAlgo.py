import pandas as pd
from collections import deque
from copy import deepcopy

def dfs(graph, frees, vertex, seq):
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

def has_hamilton_cycle(graph):
    vertices, n = list(graph.keys()), len(graph)
    def is_valid_path(path):
        return all(vertices[i + 1] in graph[vertices[i]] for i in range(n - 1)) and vertices[-1] in graph[vertices[0]]
    def backtrack(path):
        if len(path) == n:
            return is_valid_path(path)
        for v in vertices:
            if v not in path:
                path.append(v)
                if backtrack(path):
                    return True
                path.pop()
        return False
    return backtrack([vertices[0]])

def find_hamilton_cycle(adjacency_list, start_vertex):
    def backtrack(path):
        if len(path) == len(adjacency_list) and path[0] in adjacency_list[path[-1]]:
            return path
        for next_vertex in adjacency_list[path[-1]]:
            if next_vertex not in path:
                result = backtrack(path + [next_vertex])
                if result:
                    return result
        return None
    return backtrack([start_vertex])

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
