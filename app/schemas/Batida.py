from pydantic import BaseModel

class BatidaDto(BaseModel):
    id_batida:int
    nombre:str
    latitud:float
    longitud:float
    id_zona:int
    voluntarios:list[int]
    