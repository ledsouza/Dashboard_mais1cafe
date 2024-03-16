import streamlit as st
import pandas as pd
from widgets.user_authentication import create_authenticator
from database.connection import client_connection
from tests.data_processing.dataviz import metas_evolution_plot, metas_distribution_plot
from tests.data_processing.data_processing import Filtering, DataProcessing, descritive_statistics_table
from pymongo import ASCENDING

st.set_page_config(page_title="Dashboard de Metas", layout="wide")

authenticator = create_authenticator()
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Usuário ou senha incorreto")

if authentication_status is None:
    st.warning("Por favor, insira o usuário e a senha")

if authentication_status:
    authenticator.logout("Logout", "sidebar")

    if 'client' not in st.session_state:
        mongodb_password = st.secrets['db_credential']['password']
        uri = f"mongodb+srv://ledsouza:{mongodb_password}@cluster-mais1cafe.editxaq.mongodb.net/?retryWrites=true&w=majority"
        st.session_state.client = client_connection(uri)
    
    db = st.session_state.client["db_mais1cafe"]
    collection = db["metas"]

    metas_dataframe = pd.DataFrame(collection.find({}, {"_id": 0}).sort("Data", ASCENDING))

    metas_filter = Filtering(metas_dataframe)
    filtered_dataframe = metas_filter.apply_date_query()

    transformed_dataframe = DataProcessing(filtered_dataframe).transform_to_percentage()

    metas_evolution_plot(transformed_dataframe)
    metas_distribution_plot(transformed_dataframe)

    descritive_statistics_table(transformed_dataframe)
