from .sql_interface import SqlInterface

import pymssql

class Mssql(SqlInterface):
    def __init__(self, server, database, username, password, port = None):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        if port is not None:
            self.port = port

    def connect(self):
        try:
            return pymssql.connect(server=self.server, user=self.username, password=self.password, database=self.database)
        except Exception as e:
            print(f"Error connecting to MSSQL server: {e}")

    def disconnect(self, connection):
        try:
            connection.close()
        except Exception as e:
            print(f"Error disconnecting from MSSQL server: {e}")
