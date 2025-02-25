import panel as pn
import pandas as pd
import requests

from restrack.config import API_URL
from restrack.ui.process_orders_for_display import process_orders_for_display


def orders_for_patient():
    """
    Creates a form for finding all orders for a patient.

    Args:
        user_id (int): The ID of the user creating the worklist.

    Returns:
        pn.WidgetBox: A Panel WidgetBox containing the form elements.
    """

    def submit(patient_id):
        if not patient_id.isdigit():
            return
       
        try:
            r = requests.get(f"{API_URL}/orders_for_patient/{patient_id}")
            if r.status_code == 200:
                df = pd.DataFrame(r.json())
                tab=process_orders_for_display(df)
                return tab
        except: 
            return r.status_code
          
   