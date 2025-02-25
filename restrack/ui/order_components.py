import panel as pn
import pandas as pd
import requests
from restrack.config import API_URL
from restrack.ui.process_orders_for_display import process_orders_for_display


def display_orders(worklist_id: int):
    r = requests.get(f"{API_URL}/worklist_orders/{worklist_id}")
    if r.status_code == 200:
        df = pd.DataFrame(r.json())
        tab=process_orders_for_display(df)
        return tab


    else: return (r.status_code, worklist_id)




