from collections import defaultdict, deque
from core.database.wrapper import *


def build_graph(tables):
    graph = defaultdict(lambda: [])
    for table in tables:
        neighbors = get_related_tables(table)
        graph[table] = neighbors
    return graph


def topological_sort(graph, all_tables, valid_tables=None):

    if valid_tables is None:
        valid_tables = all_tables

    visited, sorted_tables = set(), deque()
    print("invoice", "vecinos: ", graph['invoice'])
    print("advance_payment", "vecinos: ", graph['advance_payment'])

    for table in valid_tables:
        if table not in visited:
            _dfs(table, graph, visited, sorted_tables)

    return list(sorted_tables)


def _dfs(node, graph, visited, sorted_tables):
    visited.add(node)
    neighbors = graph[node]
    for neighbor in neighbors:
        if neighbor not in visited:
            _dfs(neighbor, graph, visited, sorted_tables)
    sorted_tables.appendleft(node)
