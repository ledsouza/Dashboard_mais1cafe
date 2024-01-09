import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

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

    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(usecols=range(6), ttl="60m")
    data.dropna(inplace=True)
    data['Data'] = pd.to_datetime(data['Data'], format='%m/%d/%Y')

    insert_tab, delete_tab, update_tab = st.tabs(['Insert', 'Delete', 'Update'])
    with insert_tab:
        with st.form(key="insert_data", clear_on_submit=True):
            date = st.date_input(label='Selecione uma data')
            clientes = st.number_input(label='Clientes')
            produtos = st.number_input(label='Produtos')
            pa = st.number_input(label='PA')
            ticket_medio = st.number_input(label='Ticket Médio')
            faturamento = st.number_input(label='Faturamento')

            submit_button = st.form_submit_button(label="Submeter")

            if submit_button:
                updated_data = pd.DataFrame(
                    [
                        {
                            "Data": date,
                            "Clientes": clientes,
                            "Produtos": produtos,
                            "PA": pa,
                            "Ticket Médio": ticket_medio,
                            "Faturamento": faturamento,
                        }
                    ]
                )
                updated_data['Data'] = pd.to_datetime(updated_data['Data'], format='%Y/%m/%d')
                st.dataframe(updated_data)
                st.dataframe(data)

                updated_df = pd.concat([data, updated_data], ignore_index=True)
                st.dataframe(updated_df)
                conn.update(data=updated_df)

                st.success("yes")
                

