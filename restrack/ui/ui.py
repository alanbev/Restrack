import panel as pn

from restrack.ui.user_components import create_user_form
from restrack.ui.worklist_components import create_worklist_form


# Get individual components
user_form = create_user_form()
worklist_form = create_worklist_form(user=1)


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
