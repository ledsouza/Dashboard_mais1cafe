import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Funções

def read_data(conn):
    data = conn.read(usecols=range(8), ttl="0")
    data.dropna(inplace=True)
    data["Data"] = pd.to_datetime(data["Data"], format="%m/%d/%Y")
    data.sort_values(by="Data", ascending=False, inplace=True)
    return data

def get_user_input(conn, metas_max_value, pa_max_value, selected_metas=['Clientes', 'Produtos', 'PA', 'Ticket Médio', 'Faturamento', 'Cliente/Hora', 'Clima']):
    metas = {}
    data = read_data(conn)
    
    metas = {
        'Data': pd.to_datetime(st.date_input(label='Data')),
        'Clientes': st.number_input(label='Clientes', max_value=metas_max_value) if 'Clientes' in selected_metas else data.query('Data == @metas["Data"]')['Clientes'].values[0],
        'Produtos': st.number_input(label='Produtos', max_value=metas_max_value) if 'Produtos' in selected_metas else data.query('Data == @metas["Data"]')['Produtos'].values[0],
        'PA': st.number_input(label='PA', max_value=pa_max_value) if 'PA' in selected_metas else data.query('Data == @metas["Data"]')['PA'].values[0],
        'Ticket Médio': st.number_input(label='Ticket Médio', max_value=metas_max_value) if 'Ticket Médio' in selected_metas else data.query('Data == @metas["Data"]')['Ticket Médio'].values[0],
        'Faturamento': st.number_input(label='Faturamento', max_value=metas_max_value) if 'Faturamento' in selected_metas else data.query('Data == @metas["Data"]')['Faturamento'].values[0],
        'Cliente/Hora': st.number_input(label='Cliente/Hora') if 'Cliente/Hora' in selected_metas else data.query('Data == @metas["Data"]')['Cliente/Hora'].values[0],
        'Clima': st.selectbox(label='Clima', options=['Ensolarado', 'Nublado', 'Chuvoso', 'Tempestade', 'Vendaval']) if 'Clima' in selected_metas else data.query('Data == @metas["Data"]')['Clima'].values[0]
    }
    
    return metas

def update_data(conn, data, metas):
    updated_data = pd.DataFrame([metas])
    updated_df = pd.concat([data, updated_data], ignore_index=True)
    conn.update(data=updated_df)

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
    
    metas_max_value = 3.0
    pa_max_value = 4.0    
    with insert_tab:
        with st.form(key="insert_data", clear_on_submit=True):
            metas = get_user_input(conn, metas_max_value, pa_max_value)

            submit_button = st.form_submit_button(label="Inserir dados")
            if submit_button:
                data = read_data(conn)
                if not data.query('Data == @metas["Data"]').empty:
                    st.error("Dados já existentes para a data inserida")
                else:                    
                    update_data(conn, data, metas)
                    st.success("YESSSSS")   

    with update_tab:
        with st.form(key="update_data", clear_on_submit=True):
            metas = get_user_input(conn, metas_max_value, pa_max_value)

            submit_button = st.form_submit_button(label="Atualizar dados")
            if submit_button:
                data = read_data(conn)
                if data.query('Data == @metas["Data"]').empty:
                    st.error("Data não encontrada")
                else:
                    data = data[data['Data'] != metas['Data']] # Removendo a data para atualizar
                    update_data(conn, data, metas)
                    st.success("YESSSSS")

    with delete_tab:
        with st.form(key="delete_data", clear_on_submit=True):
            date = pd.to_datetime(st.date_input(label='Data'))
            
            submit_button = st.form_submit_button(label="Deletar dados")
            if submit_button:
                data = read_data(conn)
                if data.query('Data == @date').empty:
                    st.error("Data não encontrada")
                else:
                    data = data[data['Data'] != date] # Removendo a data selecionada pelo usuário
                    conn.update(data=data)

                    st.success("YESSSSS")
    
    # Banco de dados completa
    data = read_data(conn)

    ## Processando os dados para a visualização da tabela

    ### Adicionado o dia da semana
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

    ### Alterando para porcentagem
    data[["Clientes", "Produtos", "Ticket Médio", "Faturamento"]] = (
        data[["Clientes", "Produtos", "Ticket Médio", "Faturamento"]] * 100
    )
    data = (data.style
            .format("{:.0f}%", subset=["Clientes", "Produtos", "Ticket Médio", "Faturamento"])
            .format("{:.1f}", subset=["PA"], decimal=",")
            .format("{:%d.%m.%Y}", subset=["Data"])
            .format("{:.2f}", subset=["Cliente/Hora"], decimal=",")
            )

    st.markdown("# Banco de dados")
    st.dataframe(data, hide_index=True, use_container_width=True)
    st.markdown('Na coluna Cliente/Hora, valores com 0,00 indicam que o dado não foi inserido.')
