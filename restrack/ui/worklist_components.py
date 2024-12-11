import panel as pn
from restrack.models.worklist import WorkList
import requests
import os


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").strip("/")


def create_worklist_form(user_id: int):
    def submit(event):
        if not event:
            return
        btn_create.loading = True
        try:
            data = WorkList(
                name=name.value, description=description.value, created_by=user_id
            )
            print(data.model_dump_json())
            r = requests.post(API_URL + "/worklists/", data=data.model_dump_json())

            if r.status_code != 200:
                raise requests.exceptions.HTTPError(r.status_code, request=r.request)

            print(r.json())
        except Exception as e:
            raise e
        finally:
            clear(event)
            btn_create.loading = False

    def clear(event):
        if not event:
            return
        name.value = ""
        description.value = ""
        btn_create.loading = False

    name = pn.widgets.TextInput(name="Name")
    description = pn.widgets.TextInput(name="Description")
    btn_create = pn.widgets.Button(name="Submit", button_type="success")
    btn_clear = pn.widgets.Button(name="Clear", button_type="warning")

    btn_create.on_click(submit)
    btn_clear.on_click(clear)

    # form = pn.Column(name, description, pn.Row(btn_create, btn_clear))
    form = pn.WidgetBox(
        "### Create new work list", name, description, pn.Row(btn_create, btn_clear)
    )

    return form


def display_worklist(user_id: int):
    # Get worklists for user
    if not user_id:
        return

    r = requests.get(f"{API_URL}/user_worklists/{user_id}")
    items = r.json()

    options = {i["name"]: i["id"] for i in items}

    s = pn.widgets.Select(name="Worklists", options=options)
    b = pn.widgets.Button(name=">>", button_type="primary")

    return pn.Row(s, b)
