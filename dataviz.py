import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def add_vertical_line(fig: go.Figure, dataframe: pd.DataFrame) -> go.Figure:
    """
    Adds a red dotted vertical line in y=100 to the given plotly line chart.

    Parameters:
    - fig (plotly.graph_objects.Figure): The line chart figure to add the vertical line to.
    - dataframe (pandas.DataFrame): The dataframe containing the data for the line chart.

    Returns:
    - plotly.graph_objects.Figure: The updated line chart figure with the vertical line added.
    """
    fig.add_shape(
        type="line",
        x0=dataframe["Data"].min(),
        y0=100,
        x1=dataframe["Data"].max(),
        y1=100,
        line=dict(color="red", width=1, dash="dot")
    )
    return fig

def fig_metas(dataframe: pd.DataFrame) -> None:
    """
    Generate a line chart to visualize the evolution of goals.

    Args:
        dataframe (pd.DataFrame): The input dataframe containing the data.

    Returns:
        None
    """
    fig_evolucao_metas = px.line(
        dataframe,
        x="Data",
        y=["Clientes", "Produtos", "Ticket Médio", "Faturamento"],
        labels={"variable": "Metas"},
    )
    fig_evolucao_metas.update_layout(
        title="Evolução das metas",
        xaxis_title="",
        yaxis_title="Metas (%)",
        xaxis=dict(
            range=[dataframe["Data"].min(), dataframe["Data"].max()],
            tickmode="auto",
        ),
    )
    fig_evolucao_metas.update_traces(
        mode="markers+lines",
        hovertemplate="Data: %{x}<br>Valor: %{y:.0f}%<extra></extra>",
    )

    fig_evolucao_metas = add_vertical_line(fig_evolucao_metas, dataframe)

    st.plotly_chart(fig_evolucao_metas, use_container_width=True)