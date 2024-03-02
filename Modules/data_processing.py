import streamlit as st
import pandas as pd
from datetime import datetime

class Filtering:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self._dataframe = dataframe
        self.query = None

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._dataframe
    
    @dataframe.setter
    def dataframe(self, dataframe: pd.DataFrame) -> None:
        self._dataframe = dataframe

    def filter_by_date(self) -> tuple[datetime.date, datetime.date]:
        """
        Filters the data based on a selected date range.

        Returns:
            A tuple containing the start date and end date of the selected period.
        """
        period = st.date_input(
            label="Selecione o Período",
            min_value=self.dataframe["Data"].min(),
            max_value=self.dataframe["Data"].max(),
            value=(self.dataframe["Data"].min(), self.dataframe["Data"].max()),
        )
        try:
            start_date, end_date = period
        except ValueError:
            st.error("É necessário selecionar um período válido")
            st.stop()

        return (start_date, end_date)
    
    def apply_date_query(self) -> pd.DataFrame:
            """
            Applies the date filter to the dataframe.

            This method filters the dataframe based on a specified start date and end date.
            It retrieves the start and end dates by calling the `filter_by_date` method.
            Then, it constructs a query string using the retrieved dates.
            The query string filters the dataframe to include only rows where the 'Data' column
            falls within the specified date range.
            The filtered dataframe is then assigned to the `self.dataframe` attribute.

            Returns:
                filtered_dataframe (pd.DataFrame): The filtered dataframe based on the date query.
            """
            start_date, end_date = self.filter_by_date()
            query = "@start_date <= Data <= @end_date"
            filtered_dataframe = self.dataframe.query(query)
            self.dataframe = filtered_dataframe
            return filtered_dataframe
    
    def transform_to_percentage(self) -> pd.DataFrame:
        """
        Transforms the specified columns in the dataframe to percentages.

        Returns:
            pd.DataFrame: The transformed dataframe.
        """
        self.dataframe[["Clientes", "Produtos", "Ticket Médio", "Faturamento"]] = (
            self.dataframe[["Clientes", "Produtos", "Ticket Médio", "Faturamento"]] * 100
        )
        return self.dataframe
    
def descritive_statistics_table(dataframe: pd.DataFrame) -> None:
    """
    Generates a descriptive statistics table for the selected columns in the dataframe.

    Args:
        dataframe (pandas.DataFrame): The input dataframe containing the data.

    Returns:
        None
    """
    statistics = dataframe[
        ["Clientes", "Produtos", "PA", "Ticket Médio", "Faturamento"]
    ]
    statistics = statistics.describe().rename(
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