from sqlmodel import SQLModel,Field

class BatidaEntity(SQLModel, table=True):
    __tablename__ = 'Batida'
    id:int | None = Field(default=None,primary_key=True)
    nombre:str
    latitud:float
    longitud:float
    id_zona:int
    voluntarios:list[int]

    model_config = {
        'from_attributes': True,
    }