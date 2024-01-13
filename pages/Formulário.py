import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(layout="wide")

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

    insert_tab, update_tab, delete_tab = st.tabs(['Inserir', 'Atualizar', 'Deletar'])
    
    with insert_tab:
        with st.form(key="insert_data", clear_on_submit=True):
            date = st.date_input(label='Data')
            date = pd.to_datetime(date)
            clientes = st.number_input(label='Clientes', max_value=2)
            produtos = st.number_input(label='Produtos', max_value=2)
            pa = st.number_input(label='PA', max_value=4)
            ticket_medio = st.number_input(label='Ticket Médio', max_value=2)
            faturamento = st.number_input(label='Faturamento', max_value=2)

            submit_button = st.form_submit_button(label="Inserir dados")

            if submit_button:
                data = conn.read(usecols=range(6), ttl="0")
                data.dropna(inplace=True)
                data['Data'] = pd.to_datetime(data['Data'], format='%m/%d/%Y')
                if not data.query('Data == @date').empty:
                    st.error("Dados já existentes para a data inserida")
                else:
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

                    updated_df = pd.concat([data, updated_data], ignore_index=True)
                    conn.update(data=updated_df)

                    st.success("YESSSSS")

    with update_tab:
        with st.form(key="update_data", clear_on_submit=True):
            date = st.date_input(label='Data')
            date = pd.to_datetime(date)
            clientes = st.number_input(label='Clientes')
            produtos = st.number_input(label='Produtos')
            pa = st.number_input(label='PA')
            ticket_medio = st.number_input(label='Ticket Médio')
            faturamento = st.number_input(label='Faturamento')

            submit_button = st.form_submit_button(label="Atualizar dados")

            if submit_button:
                data = conn.read(usecols=range(6), ttl="0")
                data.dropna(inplace=True)
                data['Data'] = pd.to_datetime(data['Data'], format='%m/%d/%Y')
                if data.query('Data == @date').empty:
                    st.error("Data não encontrada")
                else:
                    update_data = data[data['Data'] != date]
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

                    updated_df = pd.concat([update_data, updated_data], ignore_index=True)
                    conn.update(data=updated_df)

                    st.success("YESSSSS")

    with delete_tab:
        with st.form(key="delete_data", clear_on_submit=True):
            date = st.date_input(label='Data')
            date = pd.to_datetime(date)
            
            submit_button = st.form_submit_button(label="Deletar dados")

            if submit_button:
                data = conn.read(usecols=range(6), ttl="0")
                data.dropna(inplace=True)
                data['Data'] = pd.to_datetime(data['Data'], format='%m/%d/%Y')
                if data.query('Data == @date').empty:
                    st.error("Data não encontrada")
                else:
                    update_data = data[data['Data'] != date]
                    conn.update(data=update_data)

                    st.success("YESSSSS")
    
    data = conn.read(usecols=range(6), ttl="0")
    data.dropna(inplace=True)
    data["Data"] = pd.to_datetime(data["Data"], format="%m/%d/%Y")
    data.sort_values(by="Data", ascending=False, inplace=True)
    data[["Clientes", "Produtos", "Ticket Médio", "Faturamento"]] = (
        data[["Clientes", "Produtos", "Ticket Médio", "Faturamento"]] * 100
    )  # Alterando para porcentagem

    # Tabela de dados completa
    dias_da_semana = {
        "Monday": "Segunda-feira",
        "Tuesday": "Terça-feira",
        "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira",
        "Friday": "Sexta-feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo",
    }
    data["Dia da Semana"] = data["Data"].dt.day_name().map(dias_da_semana)
    data = (data.style
            .format("{:.0f}%", subset=["Clientes", "Produtos", "Ticket Médio", "Faturamento"])
            .format("{:.1f}", subset=["PA"], decimal=",")
            .format("{:%d.%m.%Y}", subset=["Data"])
            )

    st.markdown("# Banco de dados")
    st.dataframe(data, hide_index=True, use_container_width=True)
