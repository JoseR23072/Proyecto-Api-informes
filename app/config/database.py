from sqlmodel import create_engine, Session,SQLModel
from os import getenv
from sqlalchemy.exc import OperationalError
import time


DATABASE_URL = getenv("DATABASE_URL", "mysql+mysqlconnector://user:password@localhost/dbname")


engine = create_engine(DATABASE_URL)  # echo=False por defecto
def get_session():
    return Session(engine)
