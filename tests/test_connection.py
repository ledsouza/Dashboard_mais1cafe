from Modules.connection import client_connection, database_connection
import pytest

class TestClass:
    def test_client_connection_success(self):
        client = client_connection()
        assert client is not None

    def test_client_connection_exception(self):
        with pytest.raises(Exception):
            client_connection()

    
