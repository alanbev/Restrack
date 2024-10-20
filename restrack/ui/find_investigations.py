import panel as pn
from restrack.data_access.find_orders import orders_for_patient 
pn.extension('tabulator',sizing_mode="stretch_width", template="fast")
display_table=pn.panel("table goes here")

def show_table(event):
    print(event)
    table = pn.widgets.Tabulator(orders_for_patient(hosp_numb.value))
    table=pn.panel(table)
    print (table)
    return table

   

hosp_numb = pn.widgets.TextInput(name='Hospital number')
enter_hosp_no = pn.widgets.Button(name="Enter",button_type='primary' )

result=pn.bind(show_table, hosp_numb.param.value) 

def clickhandler(clicked):
    if clicked:
        return result
    return ""

display_table= pn.panel(pn.bind(clickhandler,enter_hosp_no))
pn.Column(
pn.Row(hosp_numb, enter_hosp_no),
pn.Row(display_table)
).servable()