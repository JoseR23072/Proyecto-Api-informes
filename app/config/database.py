from sqlmodel import create_engine, Session,SQLModel
from os import getenv
from sqlalchemy.exc import OperationalError
import time


DATABASE_URL = getenv("DATABASE_URL", "mysql+mysqlconnector://user:password@localhost/dbname")

""" 
##############################
#CODIGO PROVISIONAL --> ARREGLAR EL DOCKER FILE CODIGO QUE NO SE ENTIENDA
engine = None
retries = 10
while retries > 0:
    try:
        engine = create_engine(DATABASE_URL)
        conn = engine.connect()
        conn.close()
        print("Conexión exitosa a la base de datos")

        # Crear las tablas automáticamente si no existen

        SQLModel.metadata.create_all(bind=engine)
        break
    except OperationalError as e:
        print("No se pudo conectar a la base de datos. Reintentando...")
        retries -= 1
        time.sleep(3)

if engine is None:
    raise Exception("No se pudo conectar a la base de datos después de varios intentos.")

######################### """
engine = create_engine(DATABASE_URL)  # echo=False por defecto
def get_session():
    return Session(engine)
