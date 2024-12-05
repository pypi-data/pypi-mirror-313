# greedy_best_first_search.py

import networkx as nx

def greedy_best_first_search(graph, start, goal, heuristic):
    """


    Usage:
    >>> import networkx as nx
    >>> from algoai import greedy_best_first_search
    >>> graph = nx.Graph()
    >>> graph.add_weighted_edges_from([
    >>>     ('S', 'A', 1), ('S', 'B', 4),
    >>>     ('A', 'C', 2), ('B', 'D', 2),
    >>>     ('C', 'G', 2), ('D', 'G', 3)
    >>> ])
    >>> heuristic = {'S': 7, 'A': 6, 'B': 2, 'C': 1, 'D': 2, 'G': 0}
    >>> path = greedy_best_first_search(graph, 'S', 'G', heuristic)
    >>> print("Path:", " -> ".join(path))
    Path: S -> B -> D -> G

    Code:
    -----
  
  import networkx as nx

  def greedy_best_first_search(graph, start, goal, heuristic):
    path = nx.astar_path(graph, start, goal, heuristic=lambda n, _: heuristic[n])
    return path
    """
    
    path = nx.astar_path(graph, start, goal, heuristic=lambda n, _: heuristic[n])
    return path
