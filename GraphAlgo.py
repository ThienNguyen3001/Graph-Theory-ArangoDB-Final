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