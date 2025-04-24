from pydantic import BaseModel
from models.Batida import BatidaEntity
from typing import Optional, List
from __future__ import annotations

class BatidaDto(BaseModel):
    id_batida: Optional[int] = None
    nombre: str
    latitud: float
    longitud: float
    id_zona: int
    voluntarios: Optional[List[int]] = []

    @classmethod
    def fromEntity(cls, entidad: BatidaEntity) -> BatidaDto:
        return cls(
            id_batida=entidad.id,
            nombre=entidad.nombre,
            latitud=entidad.latitud,
            longitud=entidad.longitud,
            id_zona=entidad.id_zona,
            voluntarios=entidad.voluntarios
        )

    def toEntity(self) -> BatidaEntity:
        return BatidaEntity(
            id=self.id_batida,
            nombre=self.nombre,
            latitud=self.latitud,
            longitud=self.longitud,
            id_zona=self.id_zona,
            voluntarios=self.voluntarios 
        )
