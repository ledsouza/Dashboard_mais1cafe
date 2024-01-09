import yaml
from yaml.loader import SafeLoader

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth
import pandas as pd

# --- USER AUTHENTICATION ---
with open(".streamlit/config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Usuário ou senha incorreto")

if authentication_status is None:
    st.warning("Por favor, insira o usuário e a senha")

if authentication_status:
    authenticator.logout("Logout", "sidebar")

    # Create a connection object.
    conn = st.connection("gsheets", type=GSheetsConnection)

    data = conn.read(usecols=range(6), ttl="60m")
    data['Data'] = pd.to_datetime(data['Data'], format='%m/%d/%Y')
    data[['Clientes', 'Produtos', 'Ticket Médio', 'Faturamento']] = data[['Clientes', 'Produtos', 'Ticket Médio', 'Faturamento']] * 100 # Changing to percentage

    updated_data = st.data_editor(
        data,
        column_config={
            'Data': st.column_config.DatetimeColumn(
                'Data',
                format='DD.MM.YYYY'
            ),
            'Clientes': st.column_config.NumberColumn(
                'Clientes',
                format='%d%%'
            ),
            'Produtos': st.column_config.NumberColumn(
                'Produtos',
                format='%d%%'
            ),
            'Ticket Médio': st.column_config.NumberColumn(
                'Ticket Médio',
                format='%d%%'
            ),
            'Faturamento': st.column_config.NumberColumn(
                'Faturamento',
                format='%d%%'
            )
        }
    )

    if not data.equals(updated_data):
        updated_data[['Clientes', 'Produtos', 'Ticket Médio', 'Faturamento']] = updated_data[['Clientes', 'Produtos', 'Ticket Médio', 'Faturamento']] / 100
        conn.update(data=updated_data)