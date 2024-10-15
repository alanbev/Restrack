import panel as pn
from restrack.data_access.find_orders import orders_for_patient 
pn.extension(sizing_mode="stretch_width", template="fast")
hosp_numb = pn.widgets.IntInput(name='Hospital number')
button = pn.widgets.Button()
pn.Row(hosp_numb,button).servable()

investigation_list= orders_for_patient(hosp_numb)