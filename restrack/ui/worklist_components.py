"""
This module defines the components related to worklists in the Results Tracking Portal.

Functions:
    create_worklist_form(user_id: int): Creates a form for creating a new worklist.
    display_worklist(user_id: int): Displays the worklists associated with a specific user.

Components:
    create_worklist_form: A form for creating a new worklist.
    display_worklist: A component to display the worklists for the current user.

Usage:
    These components are used in the user interface to allow users to create and view worklists.
"""

import panel as pn
import requests
from restrack.config import API_URL


def create_worklist_form(user_id: int):
    """
    Creates a form for creating a new worklist.

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
            data = dict(
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

    form = pn.WidgetBox(name, description, pn.Row(btn_create, btn_clear))
    return form


def display_worklist(user_id: int):
    """
    Displays the worklists associated with a specific user.

    Args:
        user_id (int): The ID of the user whose worklists are to be displayed.

    Returns:
        pn.Row: A Panel Row containing the worklist selection widget and a button.
    """
    # Get worklists for user
    if not user_id:
        return

    r = requests.get(f"{API_URL}/user_worklists/{user_id}")
    items = r.json()

    options = {i["name"]: i["id"] for i in items}

    # s = pn.widgets.Select(name="Worklists", options=options)
    # b = pn.widgets.Button(name=">>", button_type="primary")

    tg = pn.widgets.ToggleGroup(
        widget_type="button",
        behavior="radio",
        options=options,
        # button_type="primary",
        orientation="vertical",
        sizing_mode="scale_width",
    )

    return tg
