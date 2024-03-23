import streamlit as st
from widgets.user_authentication import UserAuthentication

st.set_page_config(layout="centered")

user_authentication = UserAuthentication()
user_authentication.login()

if st.session_state.authentication_status is None:
    st.warning("Por favor, insira o usuário e a senha")

if st.session_state.authentication_status is False:
    st.error("Usuário ou senha incorreto")

if st.session_state.authentication_status:
    st.switch_page("pages/dashboard.py")
