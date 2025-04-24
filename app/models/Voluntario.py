from sqlmodel import SQLModel,Field

class VoluntarioEntity(SQLModel,table=True):
    __tablename__ = 'voluntario'

    id:int | None = Field(default=None,primary_key=True)
    nombre:str
    apellidos:str
    email:str
    dni:str
    numeroVoluntario:str

    model_config = {
        'from_attributes': True,
    }

