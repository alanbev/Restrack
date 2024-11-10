import panel as pn
from restrack.data_access.find_orders import orders_for_patient
from functools import partial
#from data_access import store_tags

class Find_investigations():

    def __init__(self):
        pn.extension('tabulator',sizing_mode="stretch_width", template="fast")
        self.display_handler()


    def clickhandler(self,clicked):
        if clicked:
            return self.result
        return ""
    
    def selection_saver(self,tabulator_object):
        print("function has run" )
        print (tabulator_object.selected_dataframe)
    
        

    def clickhandler2(self, clicked):
            if (clicked):
             return self.save_selection
             #store_tags(self.table.selected_dataframe)

    def show_table(self,hn):
        table = pn.widgets.Tabulator(orders_for_patient(hn),selectable='checkbox', hidden_columns=['index','order_id'])
        return table
    
 

    def display_handler(self): 
        hosp_numb = pn.widgets.TextInput(name='Hospital number', width = 200)
        enter_hosp_no = pn.widgets.Button(name="Enter",button_type='primary', width=100)
        select_button=pn.widgets.Button(name="Tag Selected Investigations", button_type='primary',width=500)
        hn=hosp_numb.param.value
        self.result = pn.bind(self.show_table, hn) 
        table = pn.bind(self.clickhandler,enter_hosp_no)
        display_table=pn.panel(table)
        self.save_selection = pn.bind(self.selection_saver, self.result)
        pn.panel(pn.bind(self.clickhandler2, select_button))

        #print("self.result", type(self.result), "table",type(table),"display_table", type(display_table))
      
        output=pn.template.GoldenTemplate(
        title="Select Investigations To Tag",
        main=[
        pn.Column(
        pn.Row(hosp_numb, enter_hosp_no),
        pn.Row(display_table),
        pn.Row(select_button))]
        ).servable()    

        pn.serve(output)
