import yaml
from yaml.loader import SafeLoader
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from connection import mongo_connection

# Funções


def read_data(conn):
    data = conn.read(usecols=range(8), ttl="0")
    data.dropna(inplace=True)
    data["Data"] = pd.to_datetime(data["Data"], format="%m/%d/%Y")
    data.sort_values(by="Data", ascending=False, inplace=True)
    return data


st.set_page_config(page_title="Dashboard de Metas", layout="wide")

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

authenticator = create_authenticator()
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Usuário ou senha incorreto")

if authentication_status is None:
    st.warning("Por favor, insira o usuário e a senha")

if authentication_status:
    authenticator.logout("Logout", "sidebar")

    def database_connection(collection_name: str):
        """
        Establishes a connection to the MongoDB database and returns the specified collection.

        Parameters:
        collection_name (str): The name of the collection to retrieve.

        Returns:
        collection: The specified collection from the MongoDB database.
        """
        client = mongo_connection()
        db = client["db_mais1cafe"]
        collection = db[collection_name]
        return collection
    
    collection = database_connection('metas')
    metas_df = pd.DataFrame(collection.find({}, {"_id": 0}))

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

    # Gráfico de evolução das metas
    fig_evolucao_metas = px.line(
        filtered_df,
        x="Data",
        y=["Clientes", "Produtos", "Ticket Médio", "Faturamento"],
        labels={"variable": "Metas"},
    )
    fig_evolucao_metas.update_layout(
        title="Evolução das metas",
        xaxis_title="",
        yaxis_title="Metas (%)",
        xaxis=dict(
            range=[filtered_df["Data"].min(), filtered_df["Data"].max()],
            tickmode="auto",
        ),
    )
    fig_evolucao_metas.update_traces(
        mode="markers+lines",
        hovertemplate="Data: %{x}<br>Valor: %{y:.0f}%<extra></extra>",
    )

    # Adicione uma linha vertical pontilhada vermelha em y=100%
    fig_evolucao_metas.add_shape(
        type="line",
        x0=filtered_df["Data"].min(),
        y0=100,
        x1=filtered_df["Data"].max(),
        y1=100,
        line=dict(color="red", width=1, dash="dot"),
    )

    st.plotly_chart(fig_evolucao_metas, use_container_width=True)

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

    
