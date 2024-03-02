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
    
    def apply_date_query(self) -> None:
        """
        Applies the date filter to the dataframe.

        Returns:
            None
        """
        start_date, end_date = self.filter_by_date()
        query = "@start_date <= Data <= @end_date"
        filtered_dataframe = self.dataframe.query(query)
        return filtered_dataframe