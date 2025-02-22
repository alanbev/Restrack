import panel as pn
import requests
import json
from restrack.config import API_URL


def orders_for_patient():
    """
    Creates a form for finding all orders for a patient.

    Args:
        user_id (int): The ID of the user creating the worklist.

    Returns:
        pn.WidgetBox: A Panel WidgetBox containing the form elements.
    """

    def submit(event):
        if not event:
            return
        btn_create.loading = True
        try:
            data = {
                "Patient ID": patient_id.value,
               
            }
            headers = {"Content-Type": "application/json"}
            r = requests.post(
                f"{API_URL}/worklists/",
                data=json.dumps(data),
                headers=headers
            )
            r.raise_for_status()
            print(f"Worklist created: {r.json()}")
        except Exception as e:
            print(f"Error creating worklist: {str(e)}")
        finally:
            clear(event)
            btn_create.loading = False

    def clear(event):
        if not event:
            return
        patient_id.value = ""
     
        btn_create.loading = False

    patient_id = pn.widgets.TextInput(name="Patient ID")
    btn_create = pn.widgets.Button(name="Submit", button_type="success")
    btn_clear = pn.widgets.Button(name="Clear", button_type="warning")
    btn_create.on_click(submit)
    btn_clear.on_click(clear)

    form = pn.WidgetBox(patient_id, pn.Row(btn_create, btn_clear))
    return form
