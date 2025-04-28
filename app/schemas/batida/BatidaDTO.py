from pydantic import BaseModel
from models.Batida import BatidaEntity
from typing import Optional, List
from datetime import date
from schemas.Voluntario import VoluntarioDto

class BatidaDTO(BaseModel):
    id_batida: Optional[int] = None
    nombre: str
    latitud: float
    longitud: float
    id_zona: int
    voluntarios: str
    estado: Optional[bool] = False
    fecha_evento: date
    descripcion: str

    @classmethod
    def fromEntity(cls, entidad: BatidaEntity) -> "BatidaDTO":
        return cls(
            id_batida=entidad.id,
            nombre=entidad.nombre,
            latitud=entidad.latitud,
            longitud=entidad.longitud,
            id_zona=entidad.id_zona,
            voluntarios=entidad.voluntarios,
            estado=entidad.estado,
            fecha_evento=entidad.fecha_evento,
            descripcion=entidad.descripcion
        )