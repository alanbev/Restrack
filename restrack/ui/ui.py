"""
This module defines the user interface for the Results Tracking Portal using the Panel library.
Functions:
    get_user(username): Retrieves user information from the API based on the provided username.
Components:
    user_form: A form for user-related actions.
    worklist_form: A form for creating a new worklist.
    worklist_select: A component to display the worklist for the current user.
Template:
    template: The main template for the application, using the MaterialTemplate from Panel.
Sections:
    HEADER: Placeholder for header content.
    SIDEBAR: Contains user welcome message, worklist selection, and a button to open the worklist form modal.
    MAIN: Contains the main content area with tabs for general and admin content.
    MODAL: Contains the modal dialog for the worklist form.
Event Handlers:
    open_worklist_form(event): Opens the worklist form modal when the associated button is clicked.
Usage:
    The template is made servable at the end of the script, allowing it to be served as a web application.
"""

import panel as pn
from restrack.ui.user_components import create_user_form
from restrack.ui.worklist_components import create_worklist_form, display_worklist
from restrack.ui.order_components import display_orders
import requests
import os
import pandas as pd
from dotenv import find_dotenv, load_dotenv

pn.extension("tabulator")

load_dotenv(find_dotenv())

# Get user_id of logged in user

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").strip("/")


def get_user(username):
    try:
        r = requests.get(API_URL + "/users/username/" + username)

        # if r.status_code != 200:
        #     raise requests.exceptions.HTTPError(f"Unable to get user `{username}`")

        user = r.json()
    except Exception:
        # This is a workaround and needs to be fixed at a later date.
        user = {"id": 1, "username": "admin", "email": "admin@a.com"}
    return user


current_user = get_user(pn.state.user)
pn.state.cache["current_user"] = current_user


##############################################################################
# Event Handlers
##############################################################################


def worklist_selected(event):
    if not event:
        return
    worklist_id = worklist_select[0].value
    print(worklist_id)
    r = requests.get(f"{API_URL}/worklist_orders/{worklist_id}")
    print(r)

    if r.status_code == 200:
        df = pd.DataFrame(r.json())
        print(df)

        tbl = display_orders(df)
        main_content.clear()
        main_content.append(tbl)


##############################################################################
# Get individual components
##############################################################################
user_form = create_user_form()
worklist_form = create_worklist_form(current_user.get("id", 1))
# list_worklist = display_worklist

worklist_select = display_worklist(current_user.get("id"))
worklist_select[1].on_click(worklist_selected)

# Setup template
template = pn.template.MaterialTemplate(
    title="Results Tracking Portal", site="RESTRACK", theme=pn.template.DefaultTheme
)


##############################################################################
# HEADER
##############################################################################


##############################################################################
# SIDEBAR
##############################################################################
user_welcome = pn.Column(
    f"## Welcome _{pn.state.user.title()}",
    pn.pane.HTML("<hr>"),
    align=("center", "center"),
)
template.sidebar.append(user_welcome)

template.sidebar.append(worklist_select)
##############################################################################
# MAIN
##############################################################################
# General content

main_content = pn.Row()

tabs = pn.Tabs(("Main", main_content), dynamic=True)


# Admin content
if pn.state.user == "admin":
    admin_content = pn.Row()
    admin_content.append(user_form)
    tabs.append(("Admin", admin_content))


template.main.append(tabs)


##############################################################################
# MODAL
##############################################################################
template.modal.append(worklist_form)


def open_worklist_form(event):
    template.modal.clear()
    template.modal.append(worklist_form)
    template.open_modal()


btn_open_worklist_modal = pn.widgets.Button(name="New work list", button_type="primary")
btn_open_worklist_modal.on_click(open_worklist_form)
template.sidebar.append(btn_open_worklist_modal)


##############################################################################
template.servable()

# pn.serve(
#     {"restrack": restrack_ui},
#     basic_auth={"admin": "admin"},
#     cookie_secret="restrack-secret",
# )
