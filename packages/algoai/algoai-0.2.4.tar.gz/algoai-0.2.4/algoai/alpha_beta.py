def alpha_beta_pruning(depth, index, maximizing_player, values, alpha, beta):
    """
   
    Example:
    >>> values = [3, 5, 6, 9, 1, 2, 0, -1]
    >>> print(alpha_beta_pruning(0, 0, True, values, float('-inf'), float('inf')))
    5

    code:
    -----
    def alpha_beta_pruning(depth, index, maximizing_player, values, alpha, beta):
        if depth == 3:
            return values[index]
        
        if maximizing_player:
            best = float('-inf')
            for j in range(2):
                val = alpha_beta_pruning(depth + 1, index * 2 + j, False, values, alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = float('inf')
            for j in range(2):
                val = alpha_beta_pruning(depth + 1, index * 2 + j, True, values, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best
    """
    if depth == 3:
        return values[index]
    
    if maximizing_player:
        best = float('-inf')
        for j in range(2):
            val = alpha_beta_pruning(depth + 1, index * 2 + j, False, values, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float('inf')
        for j in range(2):
            val = alpha_beta_pruning(depth + 1, index * 2 + j, True, values, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


