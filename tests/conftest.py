import pytest
import streamlit as st
import pymongo

@pytest.fixture(scope="session")
def mongodb():
    mongodb_password = st.secrets['db_credential']['password']
    uri = f"mongodb+srv://ledsouza:{mongodb_password}@cluster-mais1cafe.editxaq.mongodb.net/?retryWrites=true&w=majority"

    client = pymongo.MongoClient(uri)
    assert client.admin.command("ping")["ok"] != 0.0 # Check that the connection is okay.
    return client

@pytest.fixture
def rollback_session(mongodb):
    session = mongodb.start_session()
    session.start_transaction()
    try:
        yield session
    finally:
        session.abort_transaction()