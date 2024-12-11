# Reusable UI Components

import panel as pn
import os
from dotenv import load_dotenv, find_dotenv
from restrack.models.worklist import User
import requests

load_dotenv(find_dotenv())

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").strip("/")


def create_user_form():
    def submit(event):
        if not event:
            return
        btn_create.loading = True
        try:
            data = User(
                username=username.value, email=email.value, password=password.value
            )
            print(data.model_dump_json())
            r = requests.post(API_URL + "/users/", data=data.model_dump_json())

            if r.status_code != 200:
                raise requests.exceptions.HTTPError(r.status_code, request=r.request)

            print(r.json())
        except Exception as e:
            raise e
        finally:
            # clear_user_form()
            btn_create.loading = False

    def clear(event):
        if not event:
            return
        username.value = ""
        email.value = ""
        password.value = ""
        btn_create.loading = False

    username = pn.widgets.TextInput(name="Username")
    email = pn.widgets.TextInput(name="Email")
    password = pn.widgets.TextInput(name="Password")
    btn_create = pn.widgets.Button(name="Submit", button_type="success")
    btn_clear = pn.widgets.Button(name="Clear", button_type="warning")

    btn_create.on_click(submit)
    btn_clear.on_click(clear)

    user_form = pn.Column(username, email, password, pn.Row(btn_create, btn_clear))

    return user_form
