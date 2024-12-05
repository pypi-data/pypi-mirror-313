import heapq

def uniform_cost_search(graph, start, goal):
    """

    Example:
    >>> graph = {'S': [('A', 1), ('B', 4)], 'A': [('C', 2), ('D', 5)], 'B': [('D', 2)], 'C': [('G', 3)], 'D': [('G', 2)], 'G': []}
    >>> uniform_cost_search(graph, 'S', 'G')
    (5, ['S', 'A', 'C', 'G'])


    Code:
    -----
    import heapq

    def uniform_cost_search(graph, start, goal):
        pq, visited = [(0, start, [])], set()

        while pq:
            cost, node, path = heapq.heappop(pq)

            if node in visited:
                continue
            
            visited.add(node)
            path = path + [node]

            if node == goal:
                return cost, path
            
            for neighbor, edge_cost in graph.get(node, []):
                if neighbor not in visited:
                    heapq.heappush(pq, (cost + edge_cost, neighbor, path))

        return float("inf"), []

    """
    pq, visited = [(0, start, [])], set()

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue
        
        visited.add(node)
        path = path + [node]

        if node == goal:
            return cost, path
        
        for neighbor, edge_cost in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(pq, (cost + edge_cost, neighbor, path))

    return float("inf"), []
