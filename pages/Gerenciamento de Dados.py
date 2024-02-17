import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from connection import mongo_connection
import time

st.set_page_config(layout="wide")

# Conexão com o banco de dados
client = mongo_connection()
db = client["db_mais1cafe"]
collection = db["metas"]


def get_user_input(
    metas_max_value,
    pa_max_value,
    selected_metas=[
        "Clientes",
        "Produtos",
        "PA",
        "Ticket Médio",
        "Faturamento",
        "Cliente/Hora",
        "Clima",
    ],
):
    metas = {}

    metas["Data"] = pd.to_datetime(st.date_input(label="Data"))

    if "Clientes" in selected_metas:
        metas["Clientes"] = st.number_input(label="Clientes", max_value=metas_max_value)

    if "Produtos" in selected_metas:
        metas["Produtos"] = st.number_input(label="Produtos", max_value=metas_max_value)

    if "PA" in selected_metas:
        metas["PA"] = st.number_input(label="PA", max_value=pa_max_value)

    if "Ticket Médio" in selected_metas:
        metas["Ticket Médio"] = st.number_input(
            label="Ticket Médio", max_value=metas_max_value
        )

    if "Faturamento" in selected_metas:
        metas["Faturamento"] = st.number_input(
            label="Faturamento", max_value=metas_max_value
        )

    if "Cliente/Hora" in selected_metas:
        metas["Cliente/Hora"] = st.number_input(label="Cliente/Hora")

    if "Clima" in selected_metas:
        metas["Clima"] = st.selectbox(
            label="Clima",
            options=["Ensolarado", "Nublado", "Chuvoso", "Tempestade", "Vendaval"],
        )

    return metas


def update_meta(metas):
    query = {"Data": metas["Data"]}
    update = {"$set": metas}
    update_status = collection.update_one(query, update)
    return update_status.acknowledged


metas_max_value = 3.0
pa_max_value = 4.0


insert_tab, update_tab, delete_tab, db_tab = st.tabs(
    ["Inserir", "Atualizar", "Deletar", "Banco de Dados"]
)

with insert_tab:
    with st.form(key="insert_data", clear_on_submit=True):
        metas = get_user_input(metas_max_value, pa_max_value)
        submit_button = st.form_submit_button(label="Inserir dados")
        if submit_button:
            insert_status = collection.insert_one(metas)
            if insert_status.acknowledged:
                st.success("YESSSSS")
            else:
                st.error("Erro ao inserir os dados")

with update_tab:
    selected_metas = st.multiselect(
        label="Metas",
        options=[
            "Clientes",
            "Produtos",
            "PA",
            "Ticket Médio",
            "Faturamento",
            "Cliente/Hora",
            "Clima",
        ],
        placeholder="Selecione as metas que deseja atualizar",
    )
    if not selected_metas:
        st.error("É necessário selecionar pelo menos uma meta")
    else:
        with st.form(key="update_data", clear_on_submit=True):
            metas = get_user_input(metas_max_value, pa_max_value, selected_metas)
            submit_button = st.form_submit_button(label="Atualizar dados")
            if submit_button:
                update_status = update_meta(metas)
                if update_status:
                    st.success("YESSSSS")
                else:
                    st.error("Erro ao atualizar os dados")

with delete_tab:
    with st.form(key="delete_data", clear_on_submit=True):
        date = pd.to_datetime(st.date_input(label="Data"))
        submit_button = st.form_submit_button(label="Deletar dados")
        if submit_button:
            delete_status = collection.delete_one({"Data": date})
            if delete_status.acknowledged:
                st.success("YESSSSS")
            else:
                st.error("Erro ao deletar os dados")

with db_tab:
    metas_df = pd.DataFrame(collection.find({}, {"_id": 0})).sort_values(
        by="Data", ascending=False
    )
    st.dataframe(metas_df, hide_index=True, use_container_width=True)

#

# # --- USER AUTHENTICATION ---
# with open(".streamlit/config.yaml") as file:
#     config = yaml.load(file, Loader=SafeLoader)

#     authenticator = stauth.Authenticate(
#         config["credentials"],
#         config["cookie"]["name"],
#         config["cookie"]["key"],
#         config["cookie"]["expiry_days"],
#     )

# name, authentication_status, username = authenticator.login("Login", "main")

# if authentication_status is False:
#     st.error("Usuário ou senha incorreto")

# if authentication_status is None:
#     st.warning("Por favor, insira o usuário e a senha")

# if authentication_status:
#     authenticator.logout("Logout", "sidebar")

#     conn = st.connection("gsheets", type=GSheetsConnection)

#     insert_tab, update_tab, delete_tab = st.tabs(['Inserir', 'Atualizar', 'Deletar'])

#     metas_max_value = 3.0
#     pa_max_value = 4.0
#     with insert_tab:
#         with st.form(key="insert_data", clear_on_submit=True):
#             metas = get_user_input(conn, metas_max_value, pa_max_value)

#             submit_button = st.form_submit_button(label="Inserir dados")
#             if submit_button:
#                 data = read_data(conn)
#                 if not data.query('Data == @metas["Data"]').empty:
#                     st.error("Dados já existentes para a data inserida")
#                 else:
#                     update_data(conn, data, metas)
#                     st.success("YESSSSS")

#     with update_tab:
#         selected_metas = st.multiselect(label='Metas', options=['Clientes', 'Produtos', 'PA', 'Ticket Médio', 'Faturamento', 'Cliente/Hora', 'Clima'], placeholder='Selecione as metas que deseja atualizar')
#         if not selected_metas:
#             st.error("É necessário selecionar pelo menos uma meta")
#         else:
#             with st.form(key="update_data", clear_on_submit=True):
#                 metas = get_user_input(conn, metas_max_value, pa_max_value, selected_metas)

#                 submit_button = st.form_submit_button(label="Atualizar dados")
#                 if submit_button:
#                     data = read_data(conn)
#                     if data.query('Data == @metas["Data"]').empty:
#                         st.error("Data não encontrada")
#                     else:
#                         data = data[data['Data'] != metas['Data']] # Removendo a data para atualizar
#                         update_data(conn, data, metas)
#                         st.success("YESSSSS")

#     with delete_tab:
#         with st.form(key="delete_data", clear_on_submit=True):
#             date = pd.to_datetime(st.date_input(label='Data'))

#             submit_button = st.form_submit_button(label="Deletar dados")
#             if submit_button:
#                 data = read_data(conn)
#                 if data.query('Data == @date').empty:
#                     st.error("Data não encontrada")
#                 else:
#                     data = data[data['Data'] != date] # Removendo a data selecionada pelo usuário
#                     conn.update(data=data)

#                     st.success("YESSSSS")

#     # Banco de dados completa
#     data = read_data(conn)

#     ## Processando os dados para a visualização da tabela

#     ### Adicionado o dia da semana
#     dias_da_semana = {
#         "Monday": "Segunda-feira",
#         "Tuesday": "Terça-feira",
#         "Wednesday": "Quarta-feira",
#         "Thursday": "Quinta-feira",
#         "Friday": "Sexta-feira",
#         "Saturday": "Sábado",
#         "Sunday": "Domingo",
#     }
#     data["Dia da Semana"] = data["Data"].dt.day_name().map(dias_da_semana)

#     ### Alterando para porcentagem
#     data[["Clientes", "Produtos", "Ticket Médio", "Faturamento"]] = (
#         data[["Clientes", "Produtos", "Ticket Médio", "Faturamento"]] * 100
#     )
#     data = (data.style
#             .format("{:.0f}%", subset=["Clientes", "Produtos", "Ticket Médio", "Faturamento"])
#             .format("{:.1f}", subset=["PA"], decimal=",")
#             .format("{:%d.%m.%Y}", subset=["Data"])
#             .format("{:.2f}", subset=["Cliente/Hora"], decimal=",")
#             )

#     st.markdown("# Banco de dados")
#     st.dataframe(data, hide_index=True, use_container_width=True)
#     st.markdown('Na coluna Cliente/Hora, valores com 0,00 indicam que o dado não foi inserido.')
