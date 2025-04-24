from pydantic import BaseModel

class ZonaDto(BaseModel):
    id:int
    nombre:str
    latitud:float
    longitud:float
    voluntariosZona:list[str]
    ciudadid:int
