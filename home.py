import streamlit as st
from widgets.user_authentication import UserAuthentication

st.set_page_config(layout="wide")

user_authentication = UserAuthentication()
user_authentication.login()
