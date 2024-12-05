

from heapq import heappop, heappush

def solve_puzzle(start, goal):
    """


    Usage:
    >>> from algoai import solve_puzzle
    >>> start = (1, 2, 3, 4, 0, 5, 6, 7, 8)
    >>> goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    >>> steps, path = solve_puzzle(start, goal)
    >>> print(f"Steps: {steps}\nPath: {path}")
    Steps: 5
    Path: ((1, 2, 3, 4, 0, 5, 6, 7, 8), (1, 2, 3, 4, 5, 0, 6, 7, 8), ...)

    Code:
    -----
    from heapq import heappop, heappush

    def solve_puzzle(start, goal):
        def h(state):
            return sum(abs((v-1) % 3 - i % 3) + abs((v-1) // 3 - i // 3) for i, v in enumerate(state) if v != 0)

        def n(state):
            idx = state.index(0)  
            neighbors = []
            for d in (-1, 1, -3, 3):  
                new_idx = idx + d
                if 0 <= new_idx < 9:

                    if (d == -1 and idx % 3 == 0) or (d == 1 and idx % 3 == 2):
                        continue

                    new_state = list(state)
                    new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                    neighbors.append(tuple(new_state))
            return neighbors


        q, visited = [(h(start), 0, start, ())], set()

        while q:
            _, cost, current_state, path = heappop(q)  
            
            if current_state in visited:
                continue
            
            if current_state == goal:
                return cost, path + (current_state,)  
            
            visited.add(current_state)
            
            for neighbor in n(current_state):
                heappush(q, (cost + h(neighbor) + 1, cost + 1, neighbor, path + (current_state,)))
        
        return -1, () 
    """
    
    def h(state):
        return sum(abs((v-1) % 3 - i % 3) + abs((v-1) // 3 - i // 3) for i, v in enumerate(state) if v != 0)

    def n(state):
        idx = state.index(0)  
        neighbors = []
        for d in (-1, 1, -3, 3):  
            new_idx = idx + d
            if 0 <= new_idx < 9:

                if (d == -1 and idx % 3 == 0) or (d == 1 and idx % 3 == 2):
                    continue

                new_state = list(state)
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                neighbors.append(tuple(new_state))
        return neighbors


    q, visited = [(h(start), 0, start, ())], set()

    while q:
        _, cost, current_state, path = heappop(q)  
        
        if current_state in visited:
            continue
        
        if current_state == goal:
            return cost, path + (current_state,)  
        
        visited.add(current_state)
        
        for neighbor in n(current_state):
            heappush(q, (cost + h(neighbor) + 1, cost + 1, neighbor, path + (current_state,)))
    
    return -1, () 


