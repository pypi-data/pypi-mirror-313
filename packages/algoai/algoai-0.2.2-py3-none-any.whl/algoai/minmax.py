def minimax_with_alpha_beta(depth, nodeIndex, maximizingPlayer, values, alpha, beta):
    """
    Example:
    >>> from algoai import minimax_with_alpha_beta
    >>> values = [3, 5, 2, 9, 12, 15, 7, 8]
    >>> print("The optimal value is:", minimax_with_alpha_beta(0, 0, True, values, float('-inf'), float('inf')))
    The optimal value is: 12

    Code:
    -----
    def minimax_with_alpha_beta(depth, nodeIndex, maximizingPlayer, values, alpha, beta):
        if depth == 3:
            return values[nodeIndex]
        
        if maximizingPlayer:
            best = float('-inf')
            for i in range(2):
                val = minimax_with_alpha_beta(depth + 1, nodeIndex * 2 + i, False, values, alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = float('inf')
            for i in range(2):
                val = minimax_with_alpha_beta(depth + 1, nodeIndex * 2 + i, True, values, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best
    """
    
    if depth == 3:
        return values[nodeIndex]
    
    if maximizingPlayer:
        best = float('-inf')
        for i in range(2):
            val = minimax_with_alpha_beta(depth + 1, nodeIndex * 2 + i, False, values, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float('inf')
        for i in range(2):
            val = minimax_with_alpha_beta(depth + 1, nodeIndex * 2 + i, True, values, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best

