from time import sleep
import pandas as pd
import streamlit as st
from pymongo.collection import Collection
from pymongo import DESCENDING
from data_processing.transformation import DataProcessing
from data_processing.dataviz import StyledDataframe
from exceptions.exceptions import DatabaseError

class FormMetas:
    """
    Class representing a form for managing goals.

    This class provides methods for retrieving user input, updating, inserting, and deleting goals in a collection.
    It also includes methods for creating forms using Streamlit and performing data processing and styling operations.

    Args:
        collection (Collection): The MongoDB collection to work with.

    Attributes:
        collection (Collection): The MongoDB collection to work with.
        metas (dict): A dictionary containing the user input for each goal.
        metas_max_value (float): The maximum value allowed for the goals.
        pa_max_value (float): The maximum value allowed for the PA goal.
        insert_tab (Streamlit Tab): The insert tab in the Streamlit app.
        update_tab (Streamlit Tab): The update tab in the Streamlit app.
        delete_tab (Streamlit Tab): The delete tab in the Streamlit app.
        database_tab (Streamlit Tab): The database tab in the Streamlit app.
        success_message (str): The success message to display.

    """

    def __init__(self, collection: Collection) -> None:
        self.collection = collection
        self.metas = {}
        self.metas_max_value = 3.0
        self.pa_max_value = 4.0
        self.insert_tab, self.update_tab, self.delete_tab, self.database_tab = st.tabs(
            ["Inserir", "Atualizar", "Deletar", "Banco de Dados"]
        )
        self.success_message = "YESSSSS"

    def get_user_input(
        self,
        selected_metas=None,
    ):
        """
        Retrieves user input for various goals.

        Args:
            selected_metas (list, optional): List of selected goals. Defaults to a predefined list.

        Returns:
            dict: A dictionary containing the user input for each goal.

        """
        if selected_metas is None:
            selected_metas = [
                "Clientes",
                "Produtos",
                "PA",
                "Ticket Médio",
                "Faturamento",
                "Cliente/Hora",
                "Clima",
            ]

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

        Args:
            session (optional): The session to use for the update operation.

        Returns:
            bool: True if the update was successful.

        Raises:
            ValueError: If the data for the selected date does not exist.

        """
        query = {"Data": self.metas["Data"]}
        update = {"$set": self.metas}
        update_status = self.collection.update_one(query, update, session=session)
        if update_status.modified_count == 0:
            raise ValueError("Os dados para a data selecionada não existem")
        else:
            st.success(self.success_message)
            return True

    def insert_meta(self, session=None):
        """
        Inserts the meta in the collection.

        This method inserts the meta data into the collection. It first checks if there is already a document with the same
        "Data" value in the collection. If a document is found, an exception is raised. Otherwise, the meta data is inserted
        into the collection using the `insert_one` method. If the insertion is successful, a success message is displayed
        using `st.success` and the method returns True. If there is an error during the insertion, an exception is raised.

        Args:
            session (optional): The session to use for the insertion. Defaults to None.

        Returns:
            bool: True if the insertion was successful.

        Raises:
            ValueError: If there is already a document with the same "Data" value in the collection.
            DatabaseError: If there is an error during the insertion.

        """
        search_result = self.collection.find_one({"Data": self.metas["Data"]})
        if search_result is not None:
            raise ValueError("Os dados para a data selecionada já existem")
        else:
            insert_status = self.collection.insert_one(self.metas, session=session)
            if insert_status.inserted_id:
                st.success(self.success_message)
                sleep(0.5)
                return True
            else:
                raise DatabaseError("Erro ao inserir os dados")

    def delete_meta(self, date, session=None):
        """
        Deletes the goal in the collection.

        Args:
            date (str): The date of the goal to be deleted.
            session (optional): The session to use for the deletion.

        Returns:
            bool: True if the deletion was successful.

        Raises:
            ValueError: If the data for the selected date does not exist.
            DatabaseError: If there was an error while deleting the data.

        """
        search_result = self.collection.find_one({"Data": date})
        if search_result is None:
            raise ValueError("Os dados para a data selecionada não existem")

        delete_status = self.collection.delete_one({"Data": date}, session=session)
        if delete_status.deleted_count == 0:
            raise DatabaseError("Erro ao deletar os dados")
        else:
            st.success(self.success_message)
            return True

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
                self.metas.clear()
                self.get_user_input()
                submit_button = st.form_submit_button(label="Inserir dados")
                if submit_button:
                    try:
                        self.insert_meta()
                    except (ValueError, DatabaseError) as e:
                        st.error(e)

    def create_update_form(self):
        """
        Creates a form for updating data in the database.

        This method creates a form using Streamlit's `st.form` function and adds user input fields.
        It also includes a submit button that, when clicked, updates the data in the database.
        If the update is successful, a success message is displayed.
        Otherwise, an error message is shown.

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
                    self.metas.clear()
                    self.get_user_input(selected_metas)
                    submit_button = st.form_submit_button(label="Atualizar dados")
                    if submit_button:
                        try:
                            self.update_meta()
                        except ValueError as e:
                            st.error(e)

    def create_delete_form(self):
        """
        Creates a form for deleting data.

        This method creates a Streamlit form that allows the user to input a date
        and delete the corresponding goal in that data from the collection.

        Returns:
            None

        """
        with self.delete_tab:
            with st.form(key="delete_data", clear_on_submit=True):
                date = pd.to_datetime(st.date_input(label="Data"))
                submit_button = st.form_submit_button(label="Deletar dados")
                if submit_button:
                    self.delete_meta(date)

    def create_database_tab(self):
        """
        Creates a database tab and performs data processing
        and styling operations on the retrieved data.

        This method retrieves data from a collection, performs data processing operations
        such as adding a week day and transforming the data to percentage,
        and applies styling to the transformed data.

        Returns:
            None

        """
        with self.database_tab:
            metas_dataframe = pd.DataFrame(
                self.collection.find({}, {"_id": 0}).sort("Data", DESCENDING)
            )
            data_processing = DataProcessing(metas_dataframe)
            data_processing.add_week_day()
            transformed_metas = data_processing.transform_to_percentage()

            metas_styler = StyledDataframe(transformed_metas)
            metas_styler.apply_style_to_metas()
