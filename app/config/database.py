from sqlmodel import create_engine, Session,SQLModel
from sqlalchemy import text
from config.settings import settings
import os

engine = create_engine(settings.DATABASE_URL)  # echo=False por defecto

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    # Ruta del archivo SQL
    sql_file_path = os.path.join(os.path.dirname(__file__), "data.sql")

    with open(sql_file_path, "r") as f:
        sql_statements = f.read()

    # Leer y ejecutar el archivo SQL
    with engine.connect() as connection:
        for statement in sql_statements.split(';'):
            statement = statement.strip()
            if statement:  # Asegurarse de que no está vacío
                connection.execute(text(statement))
        connection.commit()


def get_session():
    with Session(engine) as session:
        yield session