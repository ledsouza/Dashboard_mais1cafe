import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
from pymongo.server_api import ServerApi

def client_connection(uri) -> MongoClient:
    """
    Establishes a connection to MongoDB using the provided credentials.

    Returns:
        MongoClient: The MongoDB client object.

    Raises:
        Exception: If there is an error connecting to MongoDB.
    """
    client = MongoClient(uri, server_api=ServerApi('1'), maxIdleTimeMS=60000*10)

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)

def database_connection(client, collection_name: str) -> Collection:
        """
        Establishes a connection to the MongoDB database and returns the specified client and collection.

        Parameters:
        collection_name (str): The name of the collection to retrieve.

        Returns:
        client: The MongoDB client object.
        collection: The specified collection from the MongoDB database.
        """
        db = client["db_mais1cafe"]
        collection = db[collection_name]
        return collection
        