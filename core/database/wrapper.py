from core.database.connection import *


def get_all_tables():
    conn = DBConnection().get_connection()
    cursor = conn.cursor()
    cursor.execute("show full tables where Table_Type = 'BASE TABLE';")
    tables = [table[0] for table in cursor.fetchall()]
    return tables


def get_related_tables(table: str) -> list:
    conn = DBConnection().get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT REFERENCED_TABLE_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = '{table}';")
    neighbors = [table[0]
                 for table in cursor.fetchall() if table[0] is not None]
    return neighbors


def delete_tables(tables: list):
    for table in tables:
        try:
            delete_table(table)
            print(f"{table} table deleted.")
        except Exception as e:
            print(f"Can't delete {table} table")
            print(f"Reason: {e} table")


def delete_table(table: str):
    conn = DBConnection().get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table};")
