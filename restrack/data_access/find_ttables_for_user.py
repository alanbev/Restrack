import os
from typing import Optional
import pandas as pd
from restrack.models import user_model as um
from dotenv import find_dotenv, load_dotenv
from sqlmodel import Field, Session, SQLModel, create_engine, func, select

load_dotenv(find_dotenv())

DATABASE_CONNECTION_STRING = os.getenv("DATABASE_CONNECTION_STRING")
engine = create_engine("sqlite:///././data/users.db")

def find_ttables(user_name):
    if user_name!="":
        with Session(engine) as session:
            statement = select(um.Ttable_names.ttable_name).outerjoin_from(um.Users, um.Link_user_to_tlist, um.Users.user_number == um.Link_user_to_tlist.user.number).outerjoin_from(um.Link_user_to_tlist,um.Ttable_names,um.Link_user_to_tlist == um.Ttable_names.ttable_name).where(um.ORDER.user_name == user_name) 
            tracking_table_df= pd.read_sql(statement,session.bind)

    return tracking_table_df
    