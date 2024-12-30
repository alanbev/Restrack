import panel as pn
import pandas as pd
import requests
from restrack.config import API_URL


def display_orders(worklist_id: int):
    r = requests.get(f"{API_URL}/worklist_orders/{worklist_id}")
    if r.status_code == 200:
        df = pd.DataFrame(r.json())
    else:
        df=pd.DataFrame()

    tbl = pn.widgets.Tabulator(
        df,
        groupby=["patient_id"],
        pagination="local",
        page_size=10,
        selectable="checkbox",
        disabled=True,
    )
    return tbl
