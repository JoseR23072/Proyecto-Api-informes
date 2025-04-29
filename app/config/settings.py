# settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Definimos las variables que vamos a usar
    MICROSERVICIOS_URL: str = "http://localhost:8080/riverspain"  # Valor por defecto
    DATABASE_URL: str = "mysql+mysqlconnector://root:root@localhost:33000/informes"
    class Config:
        env_file = ".env"  # Opcional, indica que busque un fichero .env en la raíz del proyecto

# Creamos una instancia
settings = Settings()
