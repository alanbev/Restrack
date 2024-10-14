import os
from datetime import datetime
from dateutil import parser
from time import strftime
from typing import Optional

from restrack.models import cdm
from dotenv import find_dotenv, load_dotenv
from sqlmodel import Field, Session, SQLModel, create_engine, func, select

load_dotenv(find_dotenv())

DATABASE_CONNECTION_STRING = os.getenv("DATABASE_CONNECTION_STRING")


engine = create_engine(DATABASE_CONNECTION_STRING)

def orders_for_patient(patient_id):
    with Session(engine) as session:
        statement = select(cdm.ORDER).where(cdm.ORDER.patient_id==patient_id) 
        orders = session.exec(statement).all()
        orders_list=[]
        for each_order in orders:
           date=parser.parse(each_order.order_datetime)
           date.microsecond
           formated_date= date.strftime('%d/%m/%y')
           order_details=(formated_date, each_order.proc_name)
           print(order_details)
           orders_list.append(order_details)
    return orders_list
    


orders_for_patient(1176824)