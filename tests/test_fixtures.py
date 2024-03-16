from unittest.mock import MagicMock

def test_mongodb_fixture(mongodb):
    """ This test will pass if uri is set to a valid connection string. """
    assert mongodb.admin.command("ping")["ok"] > 0

def test_mock_mongodb_fixture(mock_mongodb):
    """ This test will pass if the mock_mongodb fixture is a MagicMock object. """
    assert isinstance(mock_mongodb, MagicMock)