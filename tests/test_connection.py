from Modules.connection import client_connection, database_connection
import streamlit as st
import pymongo
from unittest.mock import patch
import pytest

def test_update_mongodb(mongodb, rollback_session):
    mongodb.db_mais1cafe.metas.insert_one(
        {
            "_id": "bad_document",
            "description": "If this still exists, then transactions aren't working.",
        },
        session=rollback_session,
    )
    assert (
        mongodb.db_mais1cafe.metas.find_one(
            {"_id": "bad_document"}, session=rollback_session
        )
        != None
    )

    
