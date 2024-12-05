def depth_first_search(graph, start_node):
    """
    Example:
    >>> from algoai import depth_first_search
    >>> graph = {
    >>>     'A': ['B', 'C'],
    >>>     'B': ['D', 'E'],
    >>>     'C': ['F', 'G'],
    >>>     'D': [],
    >>>     'E': [],
    >>>     'F': [],
    >>>     'G': []
    >>> }
    >>> depth_first_search(graph, 'A')
    A B D E C F G

    Code:
    -----
    def depth_first_search(graph, start_node):
        visited = set() 

        def dfs(node):
            if node not in visited:
                print(node, end=" ")
                visited.add(node)
                for neighbor in graph[node]:
                    dfs(neighbor)

        dfs(start_node)
    """
    
    visited = set() 

    def dfs(node):
        if node not in visited:
            print(node, end=" ")
            visited.add(node)
            for neighbor in graph[node]:
                dfs(neighbor)

    dfs(start_node)

