from pydantic import BaseModel

class CiudadDto(BaseModel):
    id:int
    nombre:str
    latitud:float
    longitud:float