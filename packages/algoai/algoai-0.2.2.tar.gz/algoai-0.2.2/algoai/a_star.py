# a_star.py

from queue import PriorityQueue

def a_star_search(graph, start, goal, heuristic):
    """
    Usage:
    >>> from algoai import a_star_search
    >>> graph = {
    >>>     'S': [('A', 1), ('B', 4)],
    >>>     'A': [('C', 2)],
    >>>     'B': [('D', 2)],
    >>>     'C': [('G', 3)],
    >>>     'D': [('G', 1)],
    >>>     'G': []
    >>> }
    >>> heuristic = {
    >>>     'S': 7,
    >>>     'A': 6,
    >>>     'B': 2,
    >>>     'C': 1,
    >>>     'D': 2,
    >>>     'G': 0
    >>> }
    >>> path = a_star_search(graph, 'S', 'G', heuristic)
    >>> print("Path:", " -> ".join(path))

    Code:
    -----
    from queue import PriorityQueue

    def a_star_search(graph, start, goal, heuristic):
        open_list = PriorityQueue()
        open_list.put((0, start))  
        came_from = {}  
        g_score = {start: 0}  
        f_score = {start: heuristic[start]}  
        
        while not open_list.empty():
            current = open_list.get()[1]  
            if current == goal:

                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]  
            
            for neighbor, cost in graph[current]:
                temp_g_score = g_score[current] + cost  
                
                if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic[neighbor]
                    open_list.put((f_score[neighbor], neighbor))
                    came_from[neighbor] = current  

        return [] 
    """
    open_list = PriorityQueue()
    open_list.put((0, start))  
    came_from = {}  
    g_score = {start: 0}  
    f_score = {start: heuristic[start]}  
    
    while not open_list.empty():
        current = open_list.get()[1]  
        if current == goal:

            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  
        
        for neighbor, cost in graph[current]:
            temp_g_score = g_score[current] + cost  
            
            if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic[neighbor]
                open_list.put((f_score[neighbor], neighbor))
                came_from[neighbor] = current  

    return []  

