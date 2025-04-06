from sqlmodel import create_engine, Session,SQLModel
from os import getenv
                                    #valor predeterminados\
DATABASE_URL = getenv("DATABASE_URL", "mysql+mysqlconnector://user:password@localhost/dbname")
engine = create_engine(DATABASE_URL)  # echo=False por defecto

# Crear las tablas automáticamente si no existen
SQLModel.metadata.create_all(bind=engine)

def get_session():
    return Session(engine)
