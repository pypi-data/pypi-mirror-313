#!/usr/bin/env python3


"""
"""


import dash
import pandas as pd
import sqlite3
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
import src.ieee_papers_mapper...config.config as cfg


# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "IEEE Papers Dashboard"

def fetch_data(threshold: float = 0.5) -> pd.DataFrame:
    """
    Fetches paper counts grouped by category from the database.

    Parameters:
    ----------
    threshold : float, optional
        Minimum confidence score to filter the papers (default is 0.5).

    Returns:
    -------
    pd.DataFrame
        DataFrame containing category and count of papers.
    """
    query = f"""
        SELECT c.category, COUNT(*) as paper_count
        FROM classification c
        JOIN papers p ON c.paper_id = p.paper_id
        GROUP BY c.category
        HAVING c.confidence >= {threshold}
    """
    conn = sqlite3.connect(cfg.DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Layout for the app
app.layout = html.Div([
    html.H1("IEEE Papers by Category", style={"textAlign": "center"}),
    dcc.Graph(id="papers-bar-chart"),
    dcc.Interval(
        id="interval-component",
        interval=10 * 1000,  # Update every 10 seconds
        n_intervals=0
    )
])

# Callback to update graph
@app.callback(
    Output("papers-bar-chart", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_graph(n_intervals):
    """
    Updates the bar chart based on new data.

    Parameters:
    ----------
    n_intervals : int
        Number of times the interval has fired.

    Returns:
    -------
    plotly.graph_objects.Figure:
        Updated bar chart.
    """
    df = fetch_data()
    fig = px.bar(
        df,
        x="category",
        y="paper_count",
        title="Papers by Category",
        labels={"category": "Category", "paper_count": "Number of Papers"},
        text="paper_count"
    )
    fig.update_layout(transition_duration=500)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
