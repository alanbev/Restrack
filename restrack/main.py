import os
from typing import Optional

from restrack.models import cdm
from dotenv import find_dotenv, load_dotenv
from sqlmodel import Field, Session, SQLModel, create_engine, func, select

load_dotenv(find_dotenv())

DATABASE_CONNECTION_STRING = os.getenv("DATABASE_CONNECTION_STRING")


engine = create_engine(DATABASE_CONNECTION_STRING)

with Session(engine) as session:
    statement = select(cdm.ORDER).limit(limit=1)
    order = session.exec(statement).first()
    print(order)
