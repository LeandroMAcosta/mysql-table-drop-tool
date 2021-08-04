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
    if args.password:
        kwargs['password'] = getpass.getpass()
    
    valid_tables = kwargs.pop('tables', None)

    conn = DBConnection(**kwargs).get_connection()
    all_tables = get_all_tables()
    
    graph = build_graph(all_tables)
    sorted_tables = topological_sort(graph, all_tables, valid_tables)
    
    if set(sorted_tables) != set(valid_tables):
        difference_tables = set(sorted_tables).difference(set(valid_tables))
        print("This action also will delete next tables: ")
        print(*difference_tables, sep="\n")
        delete = input("Do you want to delete them anyway? (y/n): ")
        if delete == "y":
            delete_tables(sorted_tables)
    else:
        delete_tables(sorted_tables)


if __name__ == '__main__':
    arguments = get_arguments(sys.argv)
    main(arguments)
