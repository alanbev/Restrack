from dotenv import load_dotenv, find_dotenv
import os

from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select
import cdm

load_dotenv(find_dotenv())

DATABASE_CONNECTION_STRING = os.getenv("DATABASE_CONNECTION_STRING")


engine = create_engine(DATABASE_CONNECTION_STRING)

with Session(engine) as session:
    statement = select(cdm.CARE_SITE)
    care_site = session.exec(statement).first()
    print(care_site)
