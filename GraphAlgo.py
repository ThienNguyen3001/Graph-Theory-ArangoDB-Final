from copy import deepcopy
import pandas as pd
from collections import deque
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

def dijkstra(shortest_path, start, end):
    # Priority queue để lưu các điểm cần duyệt
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (distance, node)

    # Khoảng cách ngắn nhất từ start đến từng đỉnh
    distances = {key: float('inf') for key in shortest_path}
    distances[start] = 0

    # Để theo dõi đường đi
    previous_nodes = {key: None for key in shortest_path}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Nếu tìm thấy end, thoát vòng lặp
        if current_node == end:
            break

        # Nếu khoảng cách hiện tại lớn hơn khoảng cách đã lưu, bỏ qua
        if current_distance > distances[current_node]:
            continue

        # Duyệt tất cả các nút kề
        for neighbor, weight in shortest_path[current_node]: # Unpack the neighbor and weight
            distance = current_distance + weight  # Use the weight of the edge
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # Truy vết đường đi
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous_nodes[current]

    path.reverse()  # Đảo ngược đường đi

    # Trả về kết quả
    return path, distances[end] if distances[end] != float('inf') else None

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