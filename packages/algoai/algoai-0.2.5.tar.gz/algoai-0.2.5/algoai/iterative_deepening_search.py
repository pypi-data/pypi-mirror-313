def iterative_deepening_search(start_state, goal):
    """
    Example:
    >>>    start_state = "A"  # Starting node
    >>>    goal = "G"         # Goal node
    >>>    path = iterative_deepening_search(start_state, goal)
    >>>    if path:
    >>>        print("Path to goal:", path)
    >>>    else:
    >>>         print("Goal not found")


    code:
    ----
    class Node:
        def __init__(self, state, parent=None):
            self.state = state
            self.parent = parent
    
    def depth_limited_search(start, goal, depth):
        if start.state == goal:
            return start
        elif depth == 0:
            return None
        else:
            for child_state in get_children(start.state):
                child = Node(child_state, start)
                result = depth_limited_search(child, goal, depth - 1)
                if result is not None:
                    return result
        return None
    
    def get_children(state):
        graph = {
            "A": ["B", "C"],
            "B": ["D", "E"],
            "C": ["F", "G"],
            "D": [],
            "E": [],
            "F": [],
            "G": []
        }
        return graph.get(state, [])
    
    # Perform iterative deepening
    depth = 0
    while True:
        result = depth_limited_search(Node(start_state), goal, depth)
        if result is not None:
            # Reconstruct the path
            path = []
            while result is not None:
                path.append(result.state)
                result = result.parent
            path.reverse()
            return path  # Path to the goal
        depth += 1

    """
    
    class Node:
        def __init__(self, state, parent=None):
            self.state = state
            self.parent = parent
    
    def depth_limited_search(start, goal, depth):
        if start.state == goal:
            return start
        elif depth == 0:
            return None
        else:
            for child_state in get_children(start.state):
                child = Node(child_state, start)
                result = depth_limited_search(child, goal, depth - 1)
                if result is not None:
                    return result
        return None
    
    def get_children(state):
        graph = {
            "A": ["B", "C"],
            "B": ["D", "E"],
            "C": ["F", "G"],
            "D": [],
            "E": [],
            "F": [],
            "G": []
        }
        return graph.get(state, [])
    
    # Perform iterative deepening
    depth = 0
    while True:
        result = depth_limited_search(Node(start_state), goal, depth)
        if result is not None:
            # Reconstruct the path
            path = []
            while result is not None:
                path.append(result.state)
                result = result.parent
            path.reverse()
            return path  # Path to the goal
        depth += 1

