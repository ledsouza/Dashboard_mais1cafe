import streamlit as st
from widgets.user_authentication import create_authenticator
from database.connection import client_connection
from widgets.forms import FormMetas

st.set_page_config(layout="wide")

authenticator = create_authenticator()
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Usuário ou senha incorreto")

if authentication_status is None:
    st.warning("Por favor, insira o usuário e a senha")

if authentication_status:
    authenticator.logout("Logout", "sidebar")

    mongodb_password = st.secrets['db_credential']['password']
    uri = f"mongodb+srv://ledsouza:{mongodb_password}@cluster-mais1cafe.editxaq.mongodb.net/?retryWrites=true&w=majority"
    client = client_connection(uri)
    db = client["db_mais1cafe"]
    collection = db["metas"]

    form_metas = FormMetas(collection)

    form_metas.create_insert_form()
    form_metas.create_update_form()
    form_metas.create_delete_form()
    form_metas.create_database_tab()