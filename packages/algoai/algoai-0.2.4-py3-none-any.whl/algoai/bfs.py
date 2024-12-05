def breadth_first_search(graph, start_node):
    """

    Example:
    >>> graph = {
    >>>     'A': ['B', 'C'],
    >>>     'B': ['D', 'E'],
    >>>     'C': ['F', 'G'],
    >>>     'D': [],
    >>>     'E': [],
    >>>     'F': [],
    >>>     'G': []
    >>> }
    >>> breadth_first_search(graph, 'A')
    A B C D E F G

    Code:
    -----
    def breadth_first_search(graph, start_node):
        visited = []  
        queue = []    

        visited.append(start_node)
        queue.append(start_node)

        while queue:
            current_node = queue.pop(0)
            print(current_node, end=" ")
            for neighbor in graph[current_node]:
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.append(neighbor)
    """
    
    visited = []  
    queue = []    

    visited.append(start_node)
    queue.append(start_node)

    while queue:
        current_node = queue.pop(0)
        print(current_node, end=" ")
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)

