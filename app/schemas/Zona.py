from pydantic import BaseModel
from schemas.Voluntario import VoluntarioDto
from schemas.Ciudad import CiudadDto
from typing import List
class ZonaDto(BaseModel):
    id:int
    nombre:str
    latitud:float
    longitud:float
    voluntariosZona:List[VoluntarioDto]
    ciudad:CiudadDto
