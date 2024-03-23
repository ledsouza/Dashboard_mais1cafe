import streamlit as st
from widgets.forms import FormMetas
from widgets.user_authentication import UserAuthentication
from database.connection import client_connection

st.set_page_config(layout="wide")

authenticator = create_authenticator()
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Usuário ou senha incorreto")

if authentication_status is None:
    st.warning("Por favor, insira o usuário e a senha")

if authentication_status:
    authenticator.logout("Logout", "sidebar")

    if 'client' not in st.session_state:
        mongodb_password = st.secrets['db_credential']['password']
        uri = f"mongodb+srv://ledsouza:{mongodb_password}@cluster-mais1cafe.editxaq.mongodb.net/?retryWrites=true&w=majority"
        st.session_state.client = client_connection(uri)

    form_metas = FormMetas(st.session_state.client)

    form_metas.create_insert_form()
    form_metas.create_update_form()
    form_metas.create_delete_form()
    form_metas.create_database_tab()