import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Modules.connection import database_connection
from Modules.dataviz import metas_evolution_plot, metas_distribution_plot
from pymongo import DESCENDING, ASCENDING

# Funções

def create_authenticator():
    """
    Create an authenticator object based on the configuration specified in the .streamlit/config.yaml file.

    Returns:
        authenticator: An authenticator object configured with the credentials and cookie settings from the config file.
    """
    with open(".streamlit/config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

        authenticator = stauth.Authenticate(
            config["credentials"],
            config["cookie"]["name"],
            config["cookie"]["key"],
            config["cookie"]["expiry_days"],
        )
    return authenticator

# App

st.set_page_config(page_title="Dashboard de Metas", layout="wide")

authenticator = create_authenticator()
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Usuário ou senha incorreto")

if authentication_status is None:
    st.warning("Por favor, insira o usuário e a senha")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    
    collection = database_connection('metas')
    metas_df = pd.DataFrame(collection.find({}, {"_id": 0}).sort("Data", ASCENDING))

    periodo = st.date_input(
        label="Selecione o Período",
        min_value=metas_df["Data"].min(),
        max_value=metas_df["Data"].max(),
        value=(metas_df["Data"].min(), metas_df["Data"].max()),
    )
    try:
        start_date, end_date = periodo
    except ValueError:
        st.error("É necessário selecionar um período válido")
        st.stop()

    query = """
    @periodo[0] <= Data <= @periodo[1]
    """
    filtered_df = metas_df.query(query)

    # Processando os dados para que sejam apresentados como percentuais
    filtered_df[["Clientes", "Produtos", "Ticket Médio", "Faturamento"]] = (
        filtered_df[["Clientes", "Produtos", "Ticket Médio", "Faturamento"]] * 100
    )

    metas_evolution_plot(filtered_df)
    metas_distribution_plot(filtered_df)

    # Tabela de estatística descritiva
    filtered_statistics = filtered_df[
        ["Clientes", "Produtos", "PA", "Ticket Médio", "Faturamento"]
    ]
    statistics = filtered_statistics.describe().rename(
        index={
            "count": "Contagem Total",
            "mean": "Média",
            "std": "Desvio Padrão",
            "min": "Mínimo",
            "max": "Máximo",
        }
    )
    statistics = (
        statistics.iloc[1:, :]
        .style.format(
            "{:.0f}%", subset=["Clientes", "Produtos", "Ticket Médio", "Faturamento"]
        )
        .format("{:.1f}", subset=["PA"], decimal=",")
    )
    st.markdown("# Estatística Descritiva")
    st.dataframe(statistics, use_container_width=True)

    
