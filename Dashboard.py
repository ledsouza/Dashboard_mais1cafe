import yaml
from yaml.loader import SafeLoader

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard de Metas', layout='wide')

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

    data = conn.read(usecols=range(6), ttl="0")
    data.dropna(inplace=True)
    data['Data'] = pd.to_datetime(data['Data'], format='%m/%d/%Y')
    data.sort_values(by='Data', ascending=False, inplace=True)
    data[['Clientes', 'Produtos', 'Ticket Médio', 'Faturamento']] = data[['Clientes', 'Produtos', 'Ticket Médio', 'Faturamento']] * 100 # Changing to percentage

    # Plots
    fig_evolucao_metas = px.line(data, x='Data', y=['Clientes', 'Produtos', 'Ticket Médio', 'Faturamento'], labels={'variable': 'Metas'})
    fig_evolucao_metas.update_layout(
        title='Evolução das metas',
        xaxis_title='',
        yaxis_title='Metas (%)'
    )
    fig_evolucao_metas.update_traces(mode='markers+lines', hovertemplate='Data: %{x}<br>Valor: %{y:.0f}%<extra></extra>')

    # Add a red dotted vertical line at x=100
    fig_evolucao_metas.add_shape(
        type="line",
        x0=data['Data'].min(),
        y0=100,
        x1=data['Data'].max(),
        y1=100,
        line=dict(
            color="red",
            width=1,
            dash="dot"
        )
    )

    # App visualization
    st.plotly_chart(fig_evolucao_metas, use_container_width=True)

    st.markdown('# Banco de dados')
    st.dataframe(
        data,
        use_container_width=True,
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