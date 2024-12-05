from .sql_interface import SqlInterface

import pyodbc

class Odbc(SqlInterface):
    def __init__(self, server, database, username, password, port = None):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        if port is not None:
            self.port = port

    def connect(self, driver):
        try:
            connection_string = "DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password};".format(
                driver=driver,
                server=self.server,
                database=self.database,
                username=self.username,
                password=self.password
            )

            return pyodbc.connect(connection_string)
        except Exception as e:
            print(f"Error connecting to SQL Server: {e}")

    def disconnect(self, connection):
        try:
            connection.close()
        except Exception as e:
            print(f"Error disconnecting from SQL Server: {e}")