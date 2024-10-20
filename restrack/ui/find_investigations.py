import panel as pn
from restrack.data_access.find_orders import orders_for_patient 
pn.extension('tabulator',sizing_mode="stretch_width", template="fast")

def show_table(hn):
    print (hn)
    table = pn.widgets.Tabulator(orders_for_patient(hn),selectable='checkbox', hidden_columns=['index','order_id'])
    table=pn.panel(table)
    return table

hosp_numb = pn.widgets.TextInput(name='Hospital number', width = 200)
enter_hosp_no = pn.widgets.Button(name="Enter",button_type='primary', width=100)
hn=hosp_numb.param.value

result=pn.bind(show_table, hn) 

def clickhandler(clicked):
    if clicked:
        return result
    return ""

display_table= pn.panel(pn.bind(clickhandler,enter_hosp_no))

output=pn.template.GoldenTemplate(
title="Select Investigations To Tag",
main=[
pn.Column(
pn.Row(hosp_numb, enter_hosp_no),
pn.Row(display_table))]
).servable()

pn.serve(output)