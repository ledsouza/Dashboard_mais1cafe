import streamlit as st
import pandas as pd
from Modules.connection import database_connection
from Modules.forms import FormMetas

st.set_page_config(layout="wide")

collection = database_connection("metas")

form_metas = FormMetas(collection)

form_metas.create_insert_form()
form_metas.create_update_form()
form_metas.create_delete_form()
form_metas.create_database_tab()