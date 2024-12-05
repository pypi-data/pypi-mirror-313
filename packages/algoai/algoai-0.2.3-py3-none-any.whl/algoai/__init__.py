# Import search-related algorithms
from .a_star import a_star_search
from .bfs import breadth_first_search
from .dfs import depth_first_search
from .gbfs import greedy_best_first_search
from .uniform_cost_search import uniform_cost_search
from .memory_bounded_heuristic import ida_star
from .iterative_deepening_search import iterative_deepening_search

# Import AI algorithms
from .alpha_beta import alpha_beta_pruning
from .minmax import minimax_with_alpha_beta
from .dpll_algo import dpll_algorithm

# Import knowledge-based reasoning algorithms
from .backward_chaining import BackwardKB 
from .forward_chaining import ForwardKB 

# Import constraint satisfaction and other problem-solving algorithms
from .constraint_satisfaction_problem import map_coloring_csp
from .n_queens import n_queens_solver

# Import other miscellaneous algorithms
from .eight_puzzle import solve_puzzle
from .bayesian_network import bayesian_network
from .cryptarithmetic import cryptarithmetic
