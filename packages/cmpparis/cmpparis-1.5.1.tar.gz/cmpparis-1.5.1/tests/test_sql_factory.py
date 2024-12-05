import pytest
from cmpparis.odbc import Odbc
from cmpparis.sql_factory import SqlFactory

class TestSqlFactory:
    
    def test_create_sql_connector(self):
        sql_factory = SqlFactory()

        sql_connector = sql_factory.create_sql_connector("odbc", "test_server", "test_database", "test_username", "test_password")

        assert isinstance (sql_connector, Odbc)

    def test_create_sql_connector_error(self):
        sql_factory = SqlFactory()

        with pytest.raises(ValueError, match="Invalid connector type"):
            sql_factory.create_sql_connector("test", "test_server", "test_database", "test_username", "test_password")
