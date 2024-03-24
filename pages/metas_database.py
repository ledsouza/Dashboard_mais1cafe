import streamlit as st

from menu.menu import menu_with_redirect
from widgets.forms import FormMetas
from database.connection import client_connection

st.set_page_config(layout="wide")
menu_with_redirect()

if 'client' not in st.session_state:
    mongodb_password = st.secrets['db_credential']['password']
    uri = f"mongodb+srv://ledsouza:{mongodb_password}@cluster-mais1cafe.editxaq.mongodb.net/?retryWrites=true&w=majority"
    st.session_state.client = client_connection(uri)

form_metas = FormMetas(st.session_state.client)

form_metas.create_insert_form()
form_metas.create_update_form()
form_metas.create_delete_form()
form_metas.create_database_tab()
