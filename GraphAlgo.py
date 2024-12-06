import pandas as pd
from collections import deque

def dfs(graph,frees, vertex, seq):
    # graph: danh sách kề của đồ thị
    # frees   : trạng thái tự do (= 1) hay không (= 0) của các đỉnh (series)
    # vertex  : đỉnh đang xét duyệt (label: string)
    # seq     : chuỗi thứ tự các đỉnh đã duyệt
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

def has_euler_cycle(graph):
    """Kiểm tra chu trình Euler"""
    degrees = {}
    for vertex, neighbors in graph.items():
        degrees[vertex] = len(neighbors)
    
    return all(degree % 2 == 0 for degree in degrees.values())

def find_euler_cycle(graph):
    """Tìm chu trình Euler"""
    if not has_euler_cycle(graph):
        return None
    
    g = {k: list(v) for k, v in graph.items()}
    cycle = []
    stack = [list(g.keys())[0]]
    
    while stack:
        current = stack[-1]
        if not g[current]:
            cycle.append(current)
            stack.pop()
        else:
            neighbor = g[current].pop(0)
            for idx, edges in enumerate(g[neighbor]):
                if edges == current:
                    g[neighbor].pop(idx)
                    break
            stack.append(neighbor)
    
    return cycle[::-1]

def has_hamilton_cycle(graph):
    """Kiểm tra chu trình Hamilton"""
    vertices = list(graph.keys())
    n = len(vertices)
    
    def is_valid_path(path):
        for i in range(n - 1):
            if vertices[i + 1] not in graph[vertices[i]]:
                return False
        return vertices[-1] in graph[vertices[0]]
    
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

def bfs(graph, start):
    """Thuật toán Duyệt Rộng (Breadth-First Search)"""
    visited = set()
    queue = deque([start])
    traversal_order = []
    
    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            traversal_order.append(vertex)
            
            queue.extend(
                neighbor for neighbor in graph.get(vertex, []) 
                if neighbor not in visited
            )
    
    return traversal_order