import yaml
from yaml.loader import SafeLoader

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard de Metas', layout='wide')

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
    data['Data'] = pd.to_datetime(data['Data'], format='%m/%d/%Y')
    data.sort_values(by='Data', ascending=False, inplace=True)
    data[['Clientes', 'Produtos', 'Ticket Médio', 'Faturamento']] = data[['Clientes', 'Produtos', 'Ticket Médio', 'Faturamento']] * 100 # Alterando para porcentagem

    st.sidebar.title('Filtros')
    with st.sidebar:
        periodo = st.date_input(label='Selecione o Período', min_value=data['Data'].min(), max_value=data['Data'].max(), value=(data['Data'].min(), data['Data'].max()))

    query = '''
    @periodo[0] <= Data <= @periodo[1]
    '''

    filtered_data = data.query(query)

    # Plots
    fig_evolucao_metas = px.line(filtered_data, x='Data', y=['Clientes', 'Produtos', 'Ticket Médio', 'Faturamento'], labels={'variable': 'Metas'})
    fig_evolucao_metas.update_layout(
        title='Evolução das metas',
        xaxis_title='',
        yaxis_title='Metas (%)'
    )
    fig_evolucao_metas.update_traces(mode='markers+lines', hovertemplate='Data: %{x}<br>Valor: %{y:.0f}%<extra></extra>')

    # Adicione uma linha vertical pontilhada vermelha em y=100
    fig_evolucao_metas.add_shape(
        type="line",
        x0=filtered_data['Data'].min(),
        y0=100,
        x1=filtered_data['Data'].max(),
        y1=100,
        line=dict(
            color="red",
            width=1,
            dash="dot"
        )
    )
    
    st.plotly_chart(fig_evolucao_metas, use_container_width=True)

    # Tabela de dados completa
    dias_da_semana = {'Monday': 'Segunda-feira', 'Tuesday': 'Terça-feira', 'Wednesday': 'Quarta-feira', 'Thursday': 'Quinta-feira', 'Friday': 'Sexta-feira', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}
    data['Dia da Semana'] = data['Data'].dt.day_name().map(dias_da_semana)

    st.markdown('# Banco de dados')

    col1, col2 = st.columns(2, gap='small')
    with col1:
        st.dataframe(
                data,
                hide_index=True,
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
    
    with col2:
        st.dataframe(data.describe().rename(index={'count': 'Contagem Total', 'mean': 'Média', 'std': 'Desvio Padrão', 'min': 'Mínimo', 'max': 'Máximo'}))

    authenticator.logout("Logout", "sidebar")