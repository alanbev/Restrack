# Use this for all Create Read Update and Delete actions on database(s)

import os

from restrack.models import cdm
from dotenv import find_dotenv, load_dotenv
from sqlmodel import Session, create_engine, select


class DatabaseOperator:
    def __init__(self):
        load_dotenv(find_dotenv())

        DATABASE_CONNECTION_STRING = os.getenv("DATABASE_CONNECTION_STRING")

        self.engine = create_engine(DATABASE_CONNECTION_STRING)

    def get_person(self, person_id: int):
        with Session(self.engine) as session:
            statement = select(cdm.PERSON).where(cdm.PERSON.person_id == person_id)
            person = session.exec(statement).first()
            return person
