import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(
    usecols=range(6),
    ttl='1m'
)

updated_data = st.data_editor(data)

if not data.equals(updated_data):
    conn.update(data=updated_data)