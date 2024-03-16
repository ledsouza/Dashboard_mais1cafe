from widgets.forms import FormMetas
from streamlit.testing.v1 import AppTest
from datetime import date
import pandas as pd
import pytest

def test_get_user_input(mongodb):
    """
    Test case for the get_user_input method of the FormMetas class.

    This test verifies that the get_user_input method of the FormMetas class
    runs without raising an exception.

    Args:
        mongodb: The MongoDB fixture.

    Returns:
        None
    """
    collection = mongodb.db_mais1cafe.metas
    form_metas = FormMetas(collection)
    at = AppTest.from_function(form_metas.get_user_input)
    at.run()
    assert not at.exception

def test_update_meta_valid_date(mongodb, rollback_session):
    """
    Test case for updating meta with a valid date.

    Args:
        mongodb: The MongoDB instance.
        rollback_session: The rollback session.

    Returns:
        None
    """
    collection = mongodb.db_mais1cafe.metas

    metas = {
        "Data": pd.to_datetime(date(2024, 1, 31)),
        "Clientes": 1.0,
        "Produtos": 1.0,
        "PA": 1.0,
        "Ticket Médio": 1.0,
        "Faturamento": 1.0,
        "Cliente/Hora": 1.0,
        "Clima": "Ensolarado"
    }

    form_metas = FormMetas(collection)
    form_metas.metas = metas

    update_status = form_metas.update_meta(session=rollback_session)
    assert update_status

def test_update_meta_invalid_date(mongodb, rollback_session):
    """
    Test case for updating meta with an invalid date.

    Args:
        mongodb: The MongoDB instance.
        rollback_session: The rollback session.

    Returns:
        None
    """
    collection = mongodb.db_mais1cafe.metas

    metas = {
        "Data": pd.to_datetime(date(2020, 1, 31)),
        "Clientes": 1.0,
        "Produtos": 1.0,
        "PA": 1.0,
        "Ticket Médio": 1.0,
        "Faturamento": 1.0,
        "Cliente/Hora": 1.0,
        "Clima": "Ensolarado"
    }

    form_metas = FormMetas(collection)
    form_metas.metas = metas

    with pytest.raises(Exception) as excinfo:
        form_metas.update_meta(session=rollback_session)
        assert str(excinfo.value) == 'Os dados para a data selecionada não existem'

def test_insert_meta_valid_date(mongodb, rollback_session):
    """
    Test case for inserting meta with a valid date.

    Args:
        mongodb: The MongoDB instance.
        rollback_session: The rollback session.

    Returns:
        None
    """
    collection = mongodb.db_mais1cafe.metas

    metas = {
        "Data": pd.to_datetime(date(2020, 1, 31)),
        "Clientes": 1.0,
        "Produtos": 1.0,
        "PA": 1.0,
        "Ticket Médio": 1.0,
        "Faturamento": 1.0,
        "Cliente/Hora": 1.0,
        "Clima": "Ensolarado"
    }

    form_metas = FormMetas(collection)
    form_metas.metas = metas

    insert_status = form_metas.insert_meta(session=rollback_session)
    assert insert_status

def test_insert_meta_valid_date_with_exception(mock_mongodb, rollback_session):
    """
    Test case for inserting meta with a valid date and an exception.

    Args:
        mongodb: The MongoDB instance.
        rollback_session: The rollback session.

    Returns:
        None
    """
    collection = mock_mongodb.db_mais1cafe.metas

    metas = {
        "Data": pd.to_datetime(date(2020, 1, 31)),
        "Clientes": 1.0,
        "Produtos": 1.0,
        "PA": 1.0,
        "Ticket Médio": 1.0,
        "Faturamento": 1.0,
        "Cliente/Hora": 1.0,
        "Clima": "Ensolarado"
    }

    form_metas = FormMetas(collection)
    form_metas.metas = metas

    with pytest.raises(Exception) as excinfo:
        form_metas.insert_meta(session=rollback_session)
        assert str(excinfo.value) == 'Erro ao inserir os dados'
    

def test_insert_meta_invalid_date(mongodb, rollback_session):
    """
    Test case for inserting meta with an invalid date.

    Args:
        mongodb: The MongoDB instance.
        rollback_session: The rollback session.

    Returns:
        None
    """
    collection = mongodb.db_mais1cafe.metas

    metas = {
        "Data": pd.to_datetime(date(2024, 1, 31)),
        "Clientes": 1.0,
        "Produtos": 1.0,
        "PA": 1.0,
        "Ticket Médio": 1.0,
        "Faturamento": 1.0,
        "Cliente/Hora": 1.0,
        "Clima": "Ensolarado"
    }

    form_metas = FormMetas(collection)
    form_metas.metas = metas

    with pytest.raises(Exception) as excinfo:
        form_metas.insert_meta(session=rollback_session)
        assert str(excinfo.value) == 'Os dados para a data selecionada já existem'
