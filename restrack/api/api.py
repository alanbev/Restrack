import os
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, create_engine, SQLModel, select, and_
from restrack.models.worklist import (
    User,
    WorkList,
    UserWorkList,
)
from contextlib import asynccontextmanager
from sqlalchemy import Engine
from typing import List

DB_RESTRACK = os.getenv("DB_RESTRACK", "sqlite:///restrack.db")

engine: Engine = create_engine(url=DB_RESTRACK)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database and table if not exists
    SQLModel.metadata.create_all(engine)
    yield
    # Clean up connection
    engine.dispose()


app = FastAPI(lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User, session: Session = Depends(get_session)):
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
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return user


@app.post("/worklists/", response_model=WorkList)
def create_worklist(worklist: WorkList, session: Session = Depends(get_session)):
    print(worklist.model_dump())
    # worklist = WorkList.model_validate(worklist)
    session.add(worklist)
    session.commit()
    session.refresh(worklist)
    return worklist


@app.get("/worklists/{worklist_id}", response_model=WorkList)
def read_worklist(worklist_id: int, session: Session = Depends(get_session)):
    worklist = session.get(WorkList, worklist_id)
    if not worklist:
        raise HTTPException(status_code=404, detail="WorkList not found")
    return worklist


@app.put("/worklists/{worklist_id}", response_model=WorkList)
def update_worklist(
    worklist_id: int, worklist: WorkList, session: Session = Depends(get_session)
):
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
def delete_worklist(worklist_id: int, session: Session = Depends(get_session)):
    worklist = session.get(WorkList, worklist_id)
    if not worklist:
        raise HTTPException(status_code=404, detail="WorkList not found")
    session.delete(worklist)
    session.commit()
    return worklist


@app.get("/user_worklists/{user_id}", response_model=List[WorkList])
def get_user_worklists(user_id: int, session: Session = Depends(get_session)):
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

    worklists = session.exec(statement)

    if not worklists:
        raise HTTPException(status_code=404, detail="WorkList not found")
    return worklists
