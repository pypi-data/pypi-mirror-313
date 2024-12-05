from .odbc import Odbc
from .mssql import Mssql

class SqlFactory:
    @staticmethod
    def create_sql_connector(connector_type, server, database, username, password):
        if connector_type == "odbc":
            return Odbc(server, database, username, password)
        elif connector_type == "mssql":
            return Mssql(server, database, username, password)
        else:
            raise ValueError("Invalid connector type")