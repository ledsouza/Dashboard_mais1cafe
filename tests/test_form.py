from widgets.forms import FormMetas
from streamlit.testing.v1 import AppTest
from datetime import date
import pandas as pd
import pytest

def script_get_user_input_default(mongodb):
    from widgets.forms import FormMetas
    from datetime import date
    import pandas as pd

    collection = mongodb.db_mais1cafe.metas
    form_metas = FormMetas(collection)
    metas = form_metas.get_user_input()

    expected_result = {
        "Data": pd.to_datetime(date.today()),
        "Clientes": 0.0,
        "Produtos": 0.0,
        "PA": 0.0,
        "Ticket Médio": 0.0,
        "Faturamento": 0.0,
        "Cliente/Hora": 0.0,
        "Clima": "Ensolarado"
    }

    if metas != expected_result:
        raise Exception(f"Expected: {expected_result}, Resulted: {metas}")

def test_get_user_input_returns_default(mongodb):
    at = AppTest.from_function(script_get_user_input_default, args=(mongodb,))
    at.run()

    assert not at.exception

def script_get_user_input_set_value(mongodb):
    from widgets.forms import FormMetas
    from datetime import date
    import pandas as pd

    collection = mongodb.db_mais1cafe.metas
    form_metas = FormMetas(collection)
    metas = form_metas.get_user_input()

    expected_default = {
        "Data": pd.to_datetime(date.today()),
        "Clientes": 0.0,
        "Produtos": 0.0,
        "PA": 0.0,
        "Ticket Médio": 0.0,
        "Faturamento": 0.0,
        "Cliente/Hora": 0.0,
        "Clima": "Ensolarado"
    }

    expected_result = {
        "Data": pd.to_datetime(date(2024, 1, 1)),
        "Clientes": 1.0,
        "Produtos": 1.0,
        "PA": 1.0,
        "Ticket Médio": 1.0,
        "Faturamento": 1.0,
        "Cliente/Hora": 1.0,
        "Clima": "Ensolarado"
    }

    if metas != expected_default:
        if metas != expected_result:
            raise Exception(f"Expected: {expected_result}, Resulted: {metas}")
        
def test_get_user_input_set_value(mongodb):
    at = AppTest.from_function(script_get_user_input_set_value, args=(mongodb,))
    at.run()

    at.date_input[0].set_value(date(2024, 1, 1))
    at.number_input[0].set_value(1.0)
    at.number_input[1].set_value(1.0)
    at.number_input[2].set_value(1.0)
    at.number_input[3].set_value(1.0)
    at.number_input[4].set_value(1.0)
    at.number_input[5].set_value(1.0)
    at.selectbox[0].set_value("Ensolarado")

    at.run()

    assert not at.exception

 # TODO: create this test   

def script_get_user_input_max_value(mongodb):
    from widgets.forms import FormMetas
    from datetime import date
    import pandas as pd

    collection = mongodb.db_mais1cafe.metas
    form_metas = FormMetas(collection)
    form_metas.get_user_input()

def test_get_user_input_max_value(mongodb):
    at = AppTest.from_function(script_get_user_input_max_value, args=(mongodb,))
    at.run()

    at.date_input[0].set_value(date(2024, 1, 1))
    at.number_input[0].set_value(10000.0)
    at.number_input[1].set_value(10000.0)
    at.number_input[2].set_value(10000.0)
    at.number_input[3].set_value(10000.0)
    at.number_input[4].set_value(10000.0)
    at.number_input[5].set_value(10000.0)
    at.selectbox[0].set_value("Ensolarado")

    at.run()

    assert not at.exception

# TODO: Fix this test
# def test_get_user_input_max_value(mongodb):
#     at = AppTest.from_function(script_get_user_input, args=(mongodb,))
#     at.run()

#     # Simulando usuário preenchendo os campos
#     at.number_input[0].set_value(10000.0).run()
#     at.number_input[1].set_value(10000.0)
#     at.number_input[2].set_value(10000.0)
#     at.number_input[3].set_value(10000.0)
#     at.number_input[4].set_value(10000.0)
#     at.number_input[5].set_value(10000.0)

#     print(at.number_input[0])

#     assert not at.exception

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

def test_delete_meta_valid_date(mongodb, rollback_session):
    """
    Test case for deleting meta with a valid date.

    Args:
        mongodb: The MongoDB instance.
        rollback_session: The rollback session.

    Returns:
        None
    """
    collection = mongodb.db_mais1cafe.metas

    form_metas = FormMetas(collection)
    test_date = pd.to_datetime(date(2024, 1, 31))

    delete_status = form_metas.delete_meta(date=test_date, session=rollback_session)
    assert delete_status

def test_delete_meta_invalid_date(mock_mongodb, rollback_session):
    """
    Test case for deleting meta with an invalid date.

    Args:
        mongodb: The MongoDB instance.
        rollback_session: The rollback session.

    Returns:
        None
    """
    collection = mock_mongodb.db_mais1cafe.metas

    form_metas = FormMetas(collection)
    test_date = pd.to_datetime(date(2020, 1, 31))

    with pytest.raises(Exception) as excinfo:
        form_metas.delete_meta(date=test_date, session=rollback_session)
        assert str(excinfo.value) == 'Os dados para a data selecionada não existem'

def test_delete_meta_error(mock_mongodb, rollback_session):
    """
    Test case for deleting meta with an error.

    Args:
        mongodb: The MongoDB instance.
        rollback_session: The rollback session.

    Returns:
        None
    """
    collection = mock_mongodb.db_mais1cafe.metas

    form_metas = FormMetas(collection)
    test_date = pd.to_datetime(date(2024, 1, 31))

    with pytest.raises(Exception) as excinfo:
        form_metas.delete_meta(date=test_date, session=rollback_session)
        assert str(excinfo.value) == 'Erro ao deletar os dados'

def test_create_insert_form_widget(mongodb):
    """
    Test case for creating the insert form.

    Args:
        mongodb: The MongoDB instance.

    Returns:
        None
    """
    collection = mongodb.db_mais1cafe.metas

    form_metas = FormMetas(collection)
    at = AppTest.from_file('widgets/forms.py')
    at.from_function(form_metas.create_insert_form)
    at.run()

    assert not at.exception

def test_create_update_form_widget(mongodb):
    """
    Test case for creating the update form.

    Args:
        mongodb: The MongoDB instance.

    Returns:
        None
    """
    collection = mongodb.db_mais1cafe.metas

    form_metas = FormMetas(collection)
    at = AppTest.from_file('widgets/forms.py')
    at.from_function(form_metas.create_update_form)
    at.run()

    assert not at.exception

def test_create_delete_form_widget(mongodb):
    """
    Test case for creating the delete form.

    Args:
        mongodb: The MongoDB instance.

    Returns:
        None
    """
    collection = mongodb.db_mais1cafe.metas

    form_metas = FormMetas(collection)
    at = AppTest.from_file('widgets/forms.py')
    at.from_function(form_metas.create_delete_form)
    at.run()

    assert not at.exception

def test_create_database_tab_widget(mongodb):
    """
    Test case for creating the database tab.

    Args:
        mongodb: The MongoDB instance.

    Returns:
        None
    """
    collection = mongodb.db_mais1cafe.metas

    form_metas = FormMetas(collection)
    at = AppTest.from_file('widgets/forms.py')
    at.from_function(form_metas.create_database_tab)
    at.run()

    assert not at.exception
