from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.langapp.config import URL_DATABASE

engine = create_engine(URL_DATABASE)

SessionMaker = sessionmaker(autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionMaker
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]
