import os
from contextlib import asynccontextmanager
from typing import List

# from restrack.models.cdm import ORDER
import pyodbc
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, and_, create_engine, select

from restrack.models.cdm import Order
from restrack.models.worklist import (
    OrderWorkList,
    User,
    UserSecure,
    UserWorkList,
    WorkList,
)

DB_RESTRACK = os.getenv("DB_RESTRACK", "sqlite:///restrack.db")
DB_OMOP = os.getenv("DB_CDM")

engine_app_db: Engine = create_engine(url=DB_RESTRACK)

# ToDo: (VC) I haven't been able to find a way of connecting to two different databases
# at the same time

# engine_cdm: Engine = create_engine(url=DB_OMOP)
# ORDER.__table__.create(engine_cdm, checkfirst=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for the FastAPI application lifespan.
    Initializes the database and disposes of the engine on shutdown.
    Args:
        app (FastAPI): The FastAPI application instance.
    """
    # Create database and table if not exists
    SQLModel.metadata.create_all(engine_app_db)
    yield
    # Clean up connection
    engine_app_db.dispose()


app = FastAPI(lifespan=lifespan)


def get_app_db_session():
    """
    Dependency that provides a database session to application database.
    Yields:
        Session: A SQLModel session connected to the database.
    """
    with Session(engine_app_db) as session:
        yield session


def get_cdm_session():
    """
    Dependency that provides a database session to the OMOP database.
    Yields:
        Session: A SQLModel session connected to the database.
    """
    with Session(engine_app_db) as session:
        yield session


@app.post("/users/", response_model=UserSecure)
def create_user(user: User, session: Session = Depends(get_app_db_session)):
    """
    Create a new user in the database.
    Args:
        user (User): The user data to be created.
        session (Session, optional): The database session dependency. Defaults to Depends(get_session).
    Returns:
        User: The created user.
    """
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/users/{user_id}", response_model=UserSecure)
def read_user(user_id: int, session: Session = Depends(get_app_db_session)):
    """
    Retrieve a user by ID.
    Args:
        user_id (int): The ID of the user to retrieve.
        session (Session, optional): The database session dependency. Defaults to Depends(get_session).
    Returns:
        User: The retrieved user.
    Raises:
        HTTPException: If the user is not found, a 404 error is raised with the message "User not found".
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/username/{username}", response_model=UserSecure)
def get_user_by_username(username: str, session: Session = Depends(get_app_db_session)):
    """
    Retrieve a user by username.
    Args:
        username (int): The username of the user to retrieve.
        session (Session, optional): The database session dependency. Defaults to Depends(get_session).
    Returns:
        User: The retrieved user.
    Raises:
        HTTPException: If the user is not found, a 404 error is raised with the message "User not found".
    """
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=User)
def update_user(
    user_id: int, user: User, session: Session = Depends(get_app_db_session)
):
    """
    Update an existing user by ID.
    Args:
        user_id (int): The ID of the user to update.
        user (User): The updated user data.
        session (Session, optional): The database session dependency. Defaults to Depends(get_session).
    Returns:
        User: The updated user.
    Raises:
        HTTPException: If the user is not found, a 404 error is raised with the message "User not found".
    """
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, session: Session = Depends(get_app_db_session)):
    """
    Delete a user by ID.
    Args:
        user_id (int): The ID of the user to delete.
        session (Session, optional): The database session dependency. Defaults to Depends(get_session).
    Returns:
        User: The deleted user.
    Raises:
        HTTPException: If the user is not found, a 404 error is raised with the message "User not found".
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return user


@app.post("/worklists/", response_model=WorkList)
def create_worklist(worklist: WorkList, session: Session = Depends(get_app_db_session)):
    """
    Create a new worklist in the database.
    Args:
        worklist (WorkList): The worklist data to be created.
        session (Session, optional): The database session dependency. Defaults to Depends(get_session).
    Returns:
        WorkList: The created worklist.
    """
    print(worklist.model_dump())
    # worklist = WorkList.model_validate(worklist)
    session.add(worklist)
    session.commit()
    session.refresh(worklist)
    return worklist


@app.get("/worklists/{worklist_id}", response_model=WorkList)
def read_worklist(worklist_id: int, session: Session = Depends(get_app_db_session)):
    """
    Retrieve a worklist by ID.
    Args:
        worklist_id (int): The ID of the worklist to retrieve.
        session (Session, optional): The database session dependency. Defaults to Depends(get_session).
    Returns:
        WorkList: The retrieved worklist.
    Raises:
        HTTPException: If the worklist is not found, a 404 error is raised with the message "WorkList not found".
    """
    worklist = session.get(WorkList, worklist_id)
    if not worklist:
        raise HTTPException(status_code=404, detail="WorkList not found")
    return worklist


@app.put("/worklists/{worklist_id}", response_model=WorkList)
def update_worklist(
    worklist_id: int, worklist: WorkList, session: Session = Depends(get_app_db_session)
):
    """
    Update an existing worklist by ID.
    Args:
        worklist_id (int): The ID of the worklist to update.
        worklist (WorkList): The updated worklist data.
        session (Session, optional): The database session dependency. Defaults to Depends(get_session).
    Returns:
        WorkList: The updated worklist.
    Raises:
        HTTPException: If the worklist is not found, a 404 error is raised with the message "WorkList not found".
    """
    db_worklist = session.get(WorkList, worklist_id)
    if not db_worklist:
        raise HTTPException(status_code=404, detail="WorkList not found")
    worklist_data = worklist.dict(exclude_unset=True)
    for key, value in worklist_data.items():
        setattr(db_worklist, key, value)
    session.add(db_worklist)
    session.commit()
    session.refresh(db_worklist)
    return db_worklist


@app.delete("/worklists/{worklist_id}", response_model=WorkList)
def delete_worklist(worklist_id: int, session: Session = Depends(get_app_db_session)):
    """
    Delete a worklist by ID.
    Args:
        worklist_id (int): The ID of the worklist to delete.
        session (Session, optional): The database session dependency. Defaults to Depends(get_session).
    Returns:
        WorkList: The deleted worklist.
    Raises:
        HTTPException: If the worklist is not found, a 404 error is raised with the message "WorkList not found".
    """
    worklist = session.get(WorkList, worklist_id)
    if not worklist:
        raise HTTPException(status_code=404, detail="WorkList not found")
    session.delete(worklist)
    session.commit()
    return worklist


@app.get("/user_worklists/{user_id}", response_model=List[WorkList])
def get_user_worklists(user_id: int, session: Session = Depends(get_app_db_session)):
    """
    Retrieve worklists associated with a specific user.
    Args:
        user_id (int): The ID of the user whose worklists are to be retrieved.
        session (Session, optional): The database session dependency. Defaults to Depends(get_session).
    Returns:
        List[WorkList]: A list of worklists associated with the user.
    Raises:
        HTTPException: If no worklists are found for the user, a 404 error is raised with the message "WorkList not found".
    """
    statement = select(WorkList).where(
        and_(UserWorkList.worklist_id == WorkList.id, UserWorkList.user_id == user_id)
    )

    worklists = session.exec(statement).fetchall()

    if not worklists:
        raise HTTPException(status_code=404, detail="WorkList not found")
    return worklists


@app.get(path="/worklist_orders/{worklist_id}", response_model=List[Order])
def get_worklist_orders(
    worklist_id: int, session: Session = Depends(get_app_db_session)
):
    """
    Fetches orders associated with a specific worklist.
    This endpoint retrieves the orders linked to a given worklist ID. It first queries the local database to get the order IDs associated with the worklist. If no order IDs are found, it returns None. Otherwise, it connects to an external database using pyodbc to fetch detailed order information.
    Args:
        worklist_id (int): The ID of the worklist for which orders are to be fetched.
        session (Session): The database session dependency.
    Returns:
        List[Order]: A list of Order objects containing detailed information about each order.
    """

    statement = select(OrderWorkList.order_id).where(
        OrderWorkList.worklist_id == worklist_id
    )

    order_ids = session.exec(statement).fetchall()

    if not order_ids:
        return

    with pyodbc.connect(DB_OMOP) as cnxn:
        o = ",".join(str(i) for i in order_ids)
        sql = f"select * from promptly.alan.src_flex__orders sfo where sfo.order_id in ({o})"

        cursor = cnxn.execute(sql)
        columns = [c[0] for c in cursor.description]
        results = []
        for row in cursor.fetchall():
            r = dict(zip(columns, row))
            results.append(Order(**r))

        return results
