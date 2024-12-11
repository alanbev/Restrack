import panel as pn
import pandas as pd


def display_orders(df: pd.DataFrame):
    tbl = pn.widgets.Tabulator(df)
    return tbl
