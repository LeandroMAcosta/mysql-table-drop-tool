from collections import defaultdict, deque
from core.database.wrapper import *


def build_graph(tables):
    graph = defaultdict(lambda: defaultdict(lambda: []))
    for table in tables:
        neighbors = get_related_tables(table)
        graph[table]['neighbors'] = neighbors
        for neighbor in neighbors:
            graph[neighbor]['inverse'].append(table)    
    return graph


def topological_sort(graph, tables):

    visited, sorted_tables = set(), deque()

    for table in tables:
        if table not in visited:
            dfs(table, graph, visited, sorted_tables)

    return list(sorted_tables)


def dfs(node, graph, visited, sorted_tables=deque(), inverse=False):
    if inverse:
        neighbors = graph[node]['inverse']
    else:
        neighbors = graph[node]['neighbors']

    visited.add(node)
    for neighbor in neighbors:
        if neighbor not in visited:
            dfs(neighbor, graph, visited, sorted_tables, inverse=inverse)
    sorted_tables.appendleft(node)
