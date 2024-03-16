import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def client_connection(uri) -> MongoClient:
    """
    Establishes a connection to MongoDB using the provided credentials.

    Returns:
        MongoClient: The MongoDB client object.

    Raises:
        Exception: If there is an error connecting to MongoDB.
    """
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        