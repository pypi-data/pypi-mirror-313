def ida_star(start_state, goal_state, heuristic_func):
    """
    
    Example:
    >>>    from algoai import ida_star
    >>>    def heuristic_func(state):
    >>>        heuristic_values = {
    >>>            'A': 7, 'B': 6, 'C': 2, 'D': 1, 'E': 3, 'F': 4, 'G': 0, 
    >>>            'H': 5, 'I': 8, 'J': 9
    >>>        }
    >>>        return heuristic_values.get(state, 0)

    >>>    start_state = 'A'
    >>>    goal_state = 'G'
    >>>    result = ida_star(start_state, goal_state, heuristic_func)

    >>>    if result:
    >>>        path = []
    >>>        current = result
    >>>        while current:
    >>>            path.append(current.state)
    >>>            current = current.parent
    >>>        print("Path to goal:", " -> ".join(path[::-1]))
    >>>        print("Total cost:", result.cost)
    >>>    else:
    >>>        print("Goal not reachable.")


    Code:
    def ida_star(start_state, goal_state, heuristic_func):
        class Node:
            def __init__(self, state, parent, cost, heuristic):
                self.state = state
                self.parent = parent
                self.cost = cost
                self.heuristic = heuristic
                self.f = cost + heuristic

        def get_successors(state):
            successors = {
                'A': [('B', 3), ('C', 6)],
                'B': [('D', 2), ('E', 4)],
                'C': [('F', 1), ('G', 5)],
                'D': [('H', 7)],
                'E': [('I', 8)],
                'F': [('J', 9)],
                'G': [],
                'H': [], 'I': [], 'J': []
            }
            return successors.get(state, [])

        def search(path, g, threshold):
            node = path[-1]
            f = g + heuristic_func(node.state)
            if f > threshold:
                return f
            if node.state == goal_state:
                return node
            min_threshold = float('inf')
            for state, cost in get_successors(node.state):
                if state not in [n.state for n in path]:
                    successor = Node(state, node, g + cost, heuristic_func(state))
                    path.append(successor)
                    temp = search(path, g + cost, threshold)
                    if isinstance(temp, Node):
                        return temp
                    min_threshold = min(min_threshold, temp)
                    path.pop()
            return min_threshold

        threshold = heuristic_func(start_state)
        start_node = Node(start_state, None, 0, heuristic_func(start_state))
        path = [start_node]
        while True:
            temp = search(path, 0, threshold)
            if isinstance(temp, Node):
                return temp
            if temp == float('inf'):
                return None
            threshold = temp

    """
    
    class Node:
        def __init__(self, state, parent, cost, heuristic):
            self.state = state
            self.parent = parent
            self.cost = cost
            self.heuristic = heuristic
            self.f = cost + heuristic

    def get_successors(state):
        successors = {
            'A': [('B', 3), ('C', 6)],
            'B': [('D', 2), ('E', 4)],
            'C': [('F', 1), ('G', 5)],
            'D': [('H', 7)],
            'E': [('I', 8)],
            'F': [('J', 9)],
            'G': [],
            'H': [], 'I': [], 'J': []
        }
        return successors.get(state, [])

    def search(path, g, threshold):
        node = path[-1]
        f = g + heuristic_func(node.state)
        if f > threshold:
            return f
        if node.state == goal_state:
            return node
        min_threshold = float('inf')
        for state, cost in get_successors(node.state):
            if state not in [n.state for n in path]:
                successor = Node(state, node, g + cost, heuristic_func(state))
                path.append(successor)
                temp = search(path, g + cost, threshold)
                if isinstance(temp, Node):
                    return temp
                min_threshold = min(min_threshold, temp)
                path.pop()
        return min_threshold

    threshold = heuristic_func(start_state)
    start_node = Node(start_state, None, 0, heuristic_func(start_state))
    path = [start_node]
    while True:
        temp = search(path, 0, threshold)
        if isinstance(temp, Node):
            return temp
        if temp == float('inf'):
            return None
        threshold = temp


