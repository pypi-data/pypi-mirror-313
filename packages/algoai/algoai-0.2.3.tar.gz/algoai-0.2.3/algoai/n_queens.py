def n_queens_solver(n):
    """

    
    Example:
    >>> n_queens_solver(4)
    Enter the number of queens: 4
    Number of solutions: 2
    Solution 1:
    . Q . .
    . . . Q
    Q . . .
    . . Q .

    Solution 2:
    . . Q .
    Q . . .
    . . . Q
    . Q . .


    Code:
    -----
    def n_queens_solver(n):
        def print_solution(board):
            for row in board:
                print(" ".join("Q" if cell else "." for cell in row))
            print()

        def is_safe(board, row, col, n):
            return not any(
                board[i][col] or 
                (col - (row - i) >= 0 and board[i][col - (row - i)]) or
                (col + (row - i) < n and board[i][col + (row - i)])
                for i in range(row)
            )

        def solve_n_queens(board, row, n, solutions):
            if row == n:
                solutions.append([row[:] for row in board])  # Found a solution
            else:
                for col in range(n):
                    if is_safe(board, row, col, n):
                        board[row][col] = 1  # Place queen
                        solve_n_queens(board, row + 1, n, solutions)  # Recurse to place queens in next row
                        board[row][col] = 0  # Backtrack

        solutions = []
        solve_n_queens([[0] * n for _ in range(n)], 0, n, solutions)

        print(f"Number of solutions: {len(solutions)}")
        for index, solution in enumerate(solutions, start=1):
            print(f"Solution {index}:")
            print_solution(solution)

        return solutions
    """
    
    def print_solution(board):
        for row in board:
            print(" ".join("Q" if cell else "." for cell in row))
        print()

    def is_safe(board, row, col, n):
        return not any(
            board[i][col] or 
            (col - (row - i) >= 0 and board[i][col - (row - i)]) or
            (col + (row - i) < n and board[i][col + (row - i)])
            for i in range(row)
        )

    def solve_n_queens(board, row, n, solutions):
        if row == n:
            solutions.append([row[:] for row in board])  # Found a solution
        else:
            for col in range(n):
                if is_safe(board, row, col, n):
                    board[row][col] = 1  # Place queen
                    solve_n_queens(board, row + 1, n, solutions)  # Recurse to place queens in next row
                    board[row][col] = 0  # Backtrack

    solutions = []
    solve_n_queens([[0] * n for _ in range(n)], 0, n, solutions)

    print(f"Number of solutions: {len(solutions)}")
    for index, solution in enumerate(solutions, start=1):
        print(f"Solution {index}:")
        print_solution(solution)

    return solutions
