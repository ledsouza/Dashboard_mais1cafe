from unittest.mock import MagicMock
import pytest
import streamlit as st
import pymongo

@pytest.fixture(scope="session")
def mongodb():
    """
    Connects to a MongoDB database using the provided credentials and returns the client object.

    Returns:
        pymongo.MongoClient: The MongoDB client object.

    Raises:
        AssertionError: If the connection to the database fails.
    """
    mongodb_password = st.secrets['db_credential']['password']
    uri = f"mongodb+srv://ledsouza:{mongodb_password}@cluster-mais1cafe.editxaq.mongodb.net/?retryWrites=true&w=majority"

    client = pymongo.MongoClient(uri)
    assert client.admin.command("ping")["ok"] != 0.0 # Check that the connection is okay.
    return client

@pytest.fixture
def mock_mongodb():
    """
    Fixture for mocking the MongoDB connection.

    This fixture creates a MagicMock object that simulates a MongoDB connection.
    It also sets the side effect of the mock object to raise an Exception with the message "Mock Exception".

    Returns:
        MagicMock: The mocked MongoDB connection object.
    """
    mock_client = MagicMock()
    mock_client.side_effect = Exception("Mock Exception")
    return mock_client

# pylint: disable=redefined-outer-name
@pytest.fixture
def rollback_session(mongodb):
    """
    Fixture that provides a rollback session for MongoDB transactions.

    This fixture starts a MongoDB session and begins a transaction. It yields the session
    object, allowing the test function to use it. After the test function completes, the
    transaction is aborted, ensuring that any changes made during the test are rolled back.

    Yields:
        pymongo.client.Session: The MongoDB session object.
    """
    session = mongodb.start_session()
    session.start_transaction()
    try:
        yield session
    finally:
        session.abort_transaction()

@pytest.fixture
def login_credentials():
    """
    Fixture for setting up the login credentials.

    This fixture sets up the login credentials for the test cases.

    Returns:
        dict: A dictionary containing the user and password.
    """
    user = st.secrets['login_credential']['user']
    password = st.secrets['login_credential']['password']
    return {"user": user, "password": password}
