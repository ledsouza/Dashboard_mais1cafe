import pandas as pd
import streamlit as st
from pymongo.collection import Collection
from pymongo import DESCENDING
from Modules.data_processing import DataProcessing
from Modules.dataviz import StyledDataframe

class FormMetas:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection
        self.metas = {}
        self.metas_max_value = 3.0
        self.pa_max_value = 4.0
        self.insert_tab, self.update_tab, self.delete_tab, self.database_tab = st.tabs(
            ["Inserir", "Atualizar", "Deletar", "Banco de Dados"]
        )

    def get_user_input(
        self,
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
        """
        Retrieves user input for various goals.

        Args:
            selected_metas (list, optional): List of selected goals. Defaults to a predefined list.

        Returns:
            dict: A dictionary containing the user input for each goal.
        """

        self.metas["Data"] = pd.to_datetime(st.date_input(label="Data"))

        if "Clientes" in selected_metas:
            self.metas["Clientes"] = st.number_input(
                label="Clientes", max_value=self.metas_max_value
            )

        if "Produtos" in selected_metas:
            self.metas["Produtos"] = st.number_input(
                label="Produtos", max_value=self.metas_max_value
            )

        if "PA" in selected_metas:
            self.metas["PA"] = st.number_input(label="PA", max_value=self.pa_max_value)

        if "Ticket Médio" in selected_metas:
            self.metas["Ticket Médio"] = st.number_input(
                label="Ticket Médio", max_value=self.metas_max_value
            )

        if "Faturamento" in selected_metas:
            self.metas["Faturamento"] = st.number_input(
                label="Faturamento", max_value=self.metas_max_value
            )

        if "Cliente/Hora" in selected_metas:
            self.metas["Cliente/Hora"] = st.number_input(label="Cliente/Hora")

        if "Clima" in selected_metas:
            self.metas["Clima"] = st.selectbox(
                label="Clima",
                options=["Ensolarado", "Nublado", "Chuvoso", "Tempestade", "Vendaval"],
            )

        return self.metas

    def update_meta(self, session=None):
        """
        Updates the goal in the collection.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = {"Data": self.metas["Data"]}
        update = {"$set": self.metas}
        update_status = self.collection.update_one(query, update, session=session)
        if update_status.modified_count == 0:
            raise Exception('Os dados para a data selecionada não existem')
        else:
            st.success("YESSSSS")
            return True
        
    def insert_meta(self, session=None):
        """
        Inserts the goal in the collection.

        Returns:
            bool: True if the insertion was successful, False otherwise.
        """
        search_result = self.collection.find_one({"Data": self.metas["Data"]})
        if search_result is not None:
            raise Exception('Os dados para a data selecionada já existem')
        else:
            insert_status = self.collection.insert_one(self.metas, session=session)
            if insert_status.inserted_id:
                st.success("YESSSSS")
                return True
            else:
                raise Exception('Erro ao inserir os dados')
    
    def create_insert_form(self):
        """
        Creates a form for inserting data into the database.

        This method creates a form using Streamlit's `st.form` function and adds user input fields.
        It also includes a submit button that, when clicked, inserts the data into the database.
        If the insertion is successful, a success message is displayed. Otherwise, an error message is shown.

        Returns:
            None
        """
        with self.insert_tab:
            with st.form(key="insert_data", clear_on_submit=True):
                self.get_user_input()
                submit_button = st.form_submit_button(label="Inserir dados")
                if submit_button:
                    self.insert_meta()

    def create_update_form(self):
        """
        Creates a form for updating data in the database.

        This method creates a form using Streamlit's `st.form` function and adds user input fields.
        It also includes a submit button that, when clicked, updates the data in the database.
        If the update is successful, a success message is displayed. Otherwise, an error message is shown.

        Returns:
            None
        """
        with self.update_tab:
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
                    self.get_user_input(selected_metas)
                    submit_button = st.form_submit_button(label="Atualizar dados")
                    if submit_button:
                        update_status = self.update_meta()
                        if update_status:
                            st.success("YESSSSS")
                        else:
                            st.error("Erro ao atualizar os dados")
    
    def create_delete_form(self):
        """
        Creates a form for deleting data.

        This method creates a Streamlit form that allows the user to input a date and delete the corresponding goal in that data from the collection.

        Returns:
            None
        """
        with self.delete_tab:
            with st.form(key="delete_data", clear_on_submit=True):
                date = pd.to_datetime(st.date_input(label="Data"))
                submit_button = st.form_submit_button(label="Deletar dados")
                if submit_button:
                    delete_status = self.collection.delete_one({"Data": date})
                    if delete_status.acknowledged:
                        st.success("YESSSSS")
                    else:
                        st.error("Erro ao deletar os dados")

    def create_database_tab(self):
        with self.database_tab:
            metas_dataframe = pd.DataFrame(self.collection.find({}, {"_id": 0}).sort("Data", DESCENDING))
            data_processing = DataProcessing(metas_dataframe)
            data_processing.add_week_day()
            transformed_metas = data_processing.transform_to_percentage()

            metas_styler = StyledDataframe(transformed_metas)
            metas_styler.apply_style_to_metas()