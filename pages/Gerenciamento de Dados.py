import streamlit as st
from Modules.user_authentication import create_authenticator
from Modules.connection import database_connection
from Modules.forms import FormMetas

st.set_page_config(layout="wide")

authenticator = create_authenticator()
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Usuário ou senha incorreto")

if authentication_status is None:
    st.warning("Por favor, insira o usuário e a senha")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    collection = database_connection("metas")

    form_metas = FormMetas(collection)

    form_metas.create_insert_form()
    form_metas.create_update_form()
    form_metas.create_delete_form()
    form_metas.create_database_tab()