from datetime import date, datetime
from typing import Optional

from pydantic import ConfigDict
from sqlmodel import Field, Integer, SQLModel

class Investigation(SQLModel, table=True):
    #__table_args__ = {"schema": "alan"}
    __tablename__ = "investigation"
    investigation_number: int = Field(default=None, primary_key=True)
    hospital_number: int   
    patient_name: Optional[str] = Field(max_length=50)
    investigation_name: Optional[str] = Field(max_length=150)
    status: Optional[str] = Field(max_length=50)
    omop_number: int

class Link_user_to_tlist(SQLModel, table=True):
     #__table_args__ = {"schema": "alan"}
    __tablename__ = "link_user_to_tlist"
    index: int = Field(default=None, primary_key=True)
    user_number: int
    ttable_number: int

class Ttable(SQLModel, table=True):
     #__table_args__ = {"schema": "alan"}
    __tablename__ = "ttable"
    index: int = Field(default=None, primary_key=True)
    ttable_number:int
    investigation_number:int

class Ttable_names(SQLModel, table=True):
     #__table_args__ = {"schema": "alan"}
    __tablename__ = "ttable_names"
    ttable_number:int = Field(default=None, primary_key=True)
    ttable_name:str = Field(max_length=50)

class Users(SQLModel, table=True):
     #__table_args__ = {"schema": "alan"}
    __tablename__ = "users"
    user_number:int = Field(default=None, primary_key=True)
    user_name:str = Field(max_length=50)
    password:str = Field(max_length=50)
    user_type:str = Field(max_length=50)

class  Removed_from_tracking (SQLModel, table=True):
    #__table_args__ = {"schema": "alan"}
    __tablename__ = "removed_from_tracking"
    user_number:int = Field(default=None, primary_key=True)
    user_name:str = Field(max_length=50)
    password:str = Field(max_length=50)
    user_type:str = Field(max_length=50)