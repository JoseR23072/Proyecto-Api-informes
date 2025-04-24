from sqlmodel import SQLModel,Field
from datetime import date
class BatidaEntity(SQLModel, table=True):
    __tablename__ = 'Batida'
    id:int | None = Field(default=None,primary_key=True)
    nombre:str
    latitud:float
    longitud:float
    id_zona:int
    voluntarios: str = Field(default="[]")
    estado: bool = Field(default=False)  # Indica si el evento ha terminado
    fecha_evento: date  #
    descripcion: str
    
    model_config = {
        'from_attributes': True,
    }