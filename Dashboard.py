import yaml
from yaml.loader import SafeLoader

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Metas", layout="wide")

# --- Autenticação do usuário ---
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
    # Crie um objeto de conexão.
    conn = st.connection("gsheets", type=GSheetsConnection)

    data = conn.read(usecols=range(6), ttl="0")
    data.dropna(inplace=True)
    data["Data"] = pd.to_datetime(data["Data"], format="%m/%d/%Y")
    data.sort_values(by="Data", ascending=False, inplace=True)
    data[["Clientes", "Produtos", "Ticket Médio", "Faturamento"]] = (
        data[["Clientes", "Produtos", "Ticket Médio", "Faturamento"]] * 100
    )  # Alterando para porcentagem

    st.sidebar.title("Filtros")
    with st.sidebar:
        periodo = st.date_input(
            label="Selecione o Período",
            min_value=data["Data"].min(),
            max_value=data["Data"].max(),
            value=(data["Data"].min(), data["Data"].max()),
        )
        try:
            start_date, end_date = periodo
        except ValueError:
            st.error("É necessário selecionar um período válido")
            st.stop()

    query = """
    @periodo[0] <= Data <= @periodo[1]
    """
    # Tabelas
    filtered_data = data.query(query)
    statistics = filtered_data.describe().rename(
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

    # Plots
    fig_evolucao_metas = px.line(
        filtered_data,
        x="Data",
        y=["Clientes", "Produtos", "Ticket Médio", "Faturamento"],
        labels={"variable": "Metas"},
    )
    fig_evolucao_metas.update_layout(
        title="Evolução das metas",
        xaxis_title="",
        yaxis_title="Metas (%)",
        xaxis=dict(
            range=[filtered_data["Data"].min(), filtered_data["Data"].max()],
            tickmode="auto",
        ),
    )
    fig_evolucao_metas.update_traces(
        mode="markers+lines",
        hovertemplate="Data: %{x}<br>Valor: %{y:.0f}%<extra></extra>",
    )

    # Adicione uma linha vertical pontilhada vermelha em y=100
    fig_evolucao_metas.add_shape(
        type="line",
        x0=filtered_data["Data"].min(),
        y0=100,
        x1=filtered_data["Data"].max(),
        y1=100,
        line=dict(color="red", width=1, dash="dot"),
    )

    st.plotly_chart(fig_evolucao_metas, use_container_width=True)

    st.dataframe(statistics, use_container_width=True)

    authenticator.logout("Logout", "sidebar")
