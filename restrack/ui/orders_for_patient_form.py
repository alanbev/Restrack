import pandas as pd
import panel as pn
import requests

from restrack.config import API_URL
from restrack.ui.process_orders_for_display import process_orders_for_display


def orders_for_patient_form(update_callback=None):
    def on_submit(event):
        try:
            patient_id = patient_id_input.value
            if not patient_id:
                if update_callback:
                    update_callback("Please enter a patient ID")
                return
            
            patient_id=int(patient_id)  
            response = requests.get(f"{API_URL}/orders_for_patient/{patient_id}")
            if response.status_code == 200:
                orders = response.json()
                if not orders:
                    if update_callback:
                        update_callback("No orders found for this patient")
                    return
                print(orders)
                df = pd.DataFrame(orders)  
                table = process_orders_for_display(df)  
                if update_callback:
                    update_callback(table)
            else:
                if update_callback:
                    update_callback(f"Error: {response.status_code}")
        except Exception as e:
            if update_callback:
                update_callback(f"Error: {str(e)}")

    patient_id_input = pn.widgets.TextInput(
        name="Patient ID",
        placeholder="Enter patient ID"
    )
    
    submit_button = pn.widgets.Button(
        name="Search",
        button_type="primary"
    )
    
    submit_button.on_click(on_submit)
    
    form = pn.Column(
        patient_id_input,
        submit_button
    )
    
    return form
