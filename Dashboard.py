import streamlit as st
import pandas as pd
from Modules.user_authentication import create_authenticator
from Modules.connection import database_connection
from Modules.dataviz import metas_evolution_plot, metas_distribution_plot
from Modules.data_processing import Filtering, descritive_statistics_table
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
    
    collection = database_connection('metas')
    metas_dataframe = pd.DataFrame(collection.find({}, {"_id": 0}).sort("Data", ASCENDING))

    metas_filter = Filtering(metas_dataframe)
    metas_filter.apply_date_query()

    filtered_dataframe = metas_filter.transform_to_percentage()

    metas_evolution_plot(filtered_dataframe)
    metas_distribution_plot(filtered_dataframe)

    descritive_statistics_table(filtered_dataframe)
