import os
from mysql import connector
from core.metaclass.Singleton import *


class DBConnection(metaclass=Singleton):

    def __init__(
        self,
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DATABASE"),
        host="localhost",
        *args, **kwargs
    ):
        self._connection = connector.connect(
            username=username, password=password, host=host, database=database)

    def get_connection(self):
        return self._connection
