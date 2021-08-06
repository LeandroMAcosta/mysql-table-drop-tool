import argparse
import getpass
import sys

from core.database.connection import *
from core.database.wrapper import *
from core.graph import *


def get_arguments(argv):
    parser = argparse.ArgumentParser(description='MySQL tables deleter')
    parser.add_argument('-H', '--host', help='The host name to use', )
    parser.add_argument('-U', '--username', help='The username to use')
    parser.add_argument('-D', '--database', help='The database name to use')
    parser.add_argument('-P', '--password', help='Request Enter password manually', action='store_true')
    parser.add_argument('-T','--tables', nargs='*', help='')
    args = parser.parse_args()
    return args


def main(args):
    global conn
    kwargs = dict(filter(lambda arg: arg[1] is not None, vars(args).items()))
    
    kwargs.pop('password')
    if not args.password:
        kwargs['password'] = getpass.getpass("Password: ")

    conn = DBConnection(**kwargs).get_connection()
    all_tables = get_all_tables()
    graph = build_graph(all_tables)

    sorted_tables = topological_sort(graph, all_tables)
    
    valid_tables = kwargs.pop('tables', None)
    if valid_tables is not None:        
        inverse_visited = set()
        for valid_table in valid_tables:
            dfs(valid_table, graph, inverse_visited, inverse=True)

        if inverse_visited != set(valid_tables):
            difference_tables = set(inverse_visited).difference(set(valid_tables))
            print("This action also will delete next tables: ")
            print(*difference_tables, sep="\n")
            delete = input("Do you want to delete them anyway? (y/n): ")
            if delete == "n":
                exit(0)

        sorted_tables = list(filter(lambda table: table in inverse_visited, sorted_tables))
    
    delete_tables(sorted_tables)

if __name__ == '__main__':
    arguments = get_arguments(sys.argv)
    main(arguments)
