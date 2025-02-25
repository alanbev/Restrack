import pandas as pd
import panel as pn



def process_orders_for_display(df):       
    df_to_view = df[["order_id",
                    "patient_id",
                    "proc_name",
                    "current_status",
                    "order_datetime",
                    "in_progress",
                    "partial",
                    "complete",
                    "supplemental"]]
                    
    df_to_view['order_datetime'] = pd.to_datetime(df_to_view['order_datetime'], format='mixed')
    df_to_view['order_datetime'] = df_to_view['order_datetime'].dt.strftime('%d/%m/%Y')
    df_to_view["in_progress"] = pd.to_datetime(df_to_view[ "in_progress"], format='mixed')
    df_to_view["in_progress"] = df_to_view[ "in_progress"].dt.strftime('%d/%m/%Y')
    df_to_view["partial"] = pd.to_datetime(df_to_view[ "partial"], format='mixed')
    df_to_view["partial"] = df_to_view[ "partial"].dt.strftime('%d/%m/%Y')
    df_to_view["complete"] = pd.to_datetime(df_to_view[ "complete"], format='mixed')
    df_to_view["complete"] = df_to_view["complete"].dt.strftime('%d/%m/%Y')
    df_to_view["supplemental"] = pd.to_datetime(df_to_view["supplemental"], format='mixed')
    df_to_view["supplemental"] = df_to_view["supplemental"].dt.strftime('%d/%m/%Y')

    tbl = pn.widgets.Tabulator(
            df_to_view,
            groupby=["patient_id"],
            hidden_columns=["index","order_id", "patient_id"],
            pagination="local",
            page_size=10,
            selectable="checkbox",
            disabled=True,
        )
    return tbl