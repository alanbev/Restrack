from datetime import datetime

from sqlalchemy import Engine
from sqlmodel import Field, Relationship, SQLModel, create_engine


class User(SQLModel, table=True):
    class User:
        """
        Represents a user in the system.

        Attributes:
            id (int | None): The ID of the user. Defaults to None.
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The password of the user.
            created_at (datetime | None): The creation date and time of the user. Defaults to the current datetime.
        """

    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    created_at: datetime | None = Field(default=datetime.now())


class Person(SQLModel, table=True):
    """
    Represents a person in the system.

    Attributes:
        person_id (int | None): The ID of the person. Defaults to None.
        name (str | None): The name of the person. Defaults to None.
        birth_datetime (datetime): The birth date and time of the person.
        mrn (str | None): The MRN (Medical Record Number) of the person. Defaults to None.
        nhsnumber (int | None): The NHS (National Health Service) number of the person. Defaults to None.
    """

    person_id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None, description="Patient Name")
    birth_datetime: datetime
    mrn: str | None = Field(default=None, description="MRN")
    nhsnumber: int | None = Field(default=None, description="NHS Number")


class Order(SQLModel, table=True):
    """
    Represents an order in the worklist.

    Attributes:
        id (int, optional): The unique identifier of the order. Defaults to None.
        name (str): The name of the order.
        description (str): The description of the order.
        person_id (int): The foreign key referencing the person associated with the order.
    """

    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    person_id: int = Field(foreign_key="person.id")


class Task(SQLModel, table=True):
    """
    Represents a task in the worklist.

    Attributes:
        worklist_id (int): The ID of the worklist associated with the task.
        order_id (int): The ID of the order associated with the task.
        comment (str): The comment for the task.
        status (int): The ID of the task status.
        created_at (datetime | None): The datetime when the task was created.
        created_by (int): The ID of the user who created the task.
        updated_at (datetime | None): The datetime when the task was last updated.
        updated_by (int): The ID of the user who last updated the task.
    """

    worklist_id: int = Field(foreign_key="worklist.id", primary_key=True)
    order_id: int = Field(foreign_key="order.id", primary_key=True)
    comment: str = Field(title="Comment")
    status: int = Field(foreign_key="lkup_taskstatus.id")
    created_at: datetime | None = Field(default=datetime.now())
    created_by: int = Field(foreign_key="user.id")
    updated_at: datetime | None = Field(default=datetime.now())
    updated_by: int = Field(foreign_key="user.id")


class WorkList(SQLModel, table=True):
    """
    Represents a work list.

    Attributes:
        id (int | None): The ID of the work list. Defaults to None.
        name (str): The name of the work list.
        description (str | None): The description of the work list. Defaults to None.
        created_by (int): The ID of the user who created the work list.
        created_at (datetime | None): The timestamp when the work list was created. Defaults to the current datetime.
        updated_at (datetime | None): The timestamp when the work list was last updated. Defaults to the current datetime.
        updated_by (int): The ID of the user who last updated the work list.
        orders (list["Order"]): The list of orders associated with the work list.
    """

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(title="Name of work list")
    description: str | None = Field(default=None, title="Description")
    created_by: int = Field(foreign_key="user.id")
    created_at: datetime | None = Field(default=datetime.now())
    created_by: int = Field(foreign_key="user.id")
    updated_at: datetime | None = Field(default=datetime.now())
    updated_by: int = Field(foreign_key="user.id")
    orders: list["Order"] = Relationship(back_populates="worklists", link_model=Task)


class Lkup_TaskStatus(SQLModel, table=True):
    """
    Represents a task status in the worklist.

    Attributes:
        id (int | None): The ID of the task status. Defaults to None.
        name (str): The name of the task status.
        description (str | None): The description of the task status. Defaults to None.
    """

    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None


engine: Engine = create_engine(url="sqlite:///restrack.db")


SQLModel.metadata.create_all(bind=engine)
