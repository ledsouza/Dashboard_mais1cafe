from Modules.forms import FormMetas
from streamlit.testing.v1 import AppTest
import pytest

def test_get_user_input(run_app: AppTest):
    form_metas = FormMetas()
    user_input = form_metas.get_user_input()
    assert user_input == {
        "Data": "2021-08-01",
        "Clientes": 1.0,
        "Produtos": 1.0,
        "PA": 1.0,
        "Ticket Médio": 1.0,
        "Faturamento": 1.0,
    }