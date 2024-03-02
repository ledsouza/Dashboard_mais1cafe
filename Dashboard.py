import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from MongoDBConnection.connection import database_connection
from dataviz import fig_metas
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

    fig_metas(filtered_df)

    # Gráfico de distribuição das metas
    metas = filtered_df.columns[1:6]
    meta = st.selectbox(label="Selecione a meta", options=metas, index=0)
    title_text = f"Distribuição da Meta de {meta}"
    fig_dist = go.Figure(
        data=[
            go.Histogram(
                x=filtered_df[meta],
                showlegend=False,
                name="",
                hovertemplate="Faixa de valores: %{x}%<br>Frequência: %{y}",
                textposition="outside",
                texttemplate="%{y}",
            )
        ]
    )
    fig_dist.update_layout(
        title=title_text,
        xaxis_title="Metas (%)",
        yaxis_title="Contagem",
        yaxis=dict(showticklabels=False),
    )
    fig_dist.update_traces(marker_line_width=1, marker_line_color="white")
    st.plotly_chart(fig_dist, use_container_width=True)

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

    
