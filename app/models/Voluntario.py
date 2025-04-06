from sqlmodel import SQLModel,Field

class Voluntario(SQLModel,table=True):
    id:int | None = Field(default=None,primary_key=True)
    nombre:str
    apellidos:str
    email:str
    dni:str
    numeroVoluntario:str