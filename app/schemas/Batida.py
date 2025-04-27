from __future__ import annotations
from pydantic import BaseModel
from models.Batida import BatidaEntity
from typing import Optional, List
from datetime import date
import json
from schemas.Voluntario import VoluntarioDto


class BatidaBase(BaseModel):
    nombre: str
    descripcion: str
    latitud: float
    longitud: float
    id_zona: int
    estado: Optional[bool] = False
    fecha_evento: date

    
class BatidaDto(BaseModel):
    id_batida: Optional[int] = None
    nombre: str
    latitud: float
    longitud: float
    id_zona: int
    voluntarios: Optional[List[VoluntarioDto]] = []
    estado: Optional[bool] = False
    fecha_evento: date
    descripcion: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Batida en el Parque Natural",
                    "latitud": 40.4168,
                    "longitud": -3.7038,
                    "id_zona": 2,
                    "estado": False,
                    "fecha_evento": "2025-04-26",
                    "descripcion": "Batida de limpieza y reforestación"
                }
            ]
        }
    }
    @classmethod
    def fromEntity(cls, entidad: BatidaEntity) -> BatidaDto:
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
    
    @classmethod
    def from_dto2(cls, dto2: "BatidaDTO2", voluntarios: List[VoluntarioDto]) -> "BatidaDto":
        return cls(
            id_batida=dto2.id_batida,
            nombre=dto2.nombre,
            latitud=dto2.latitud,
            longitud=dto2.longitud,
            id_zona=dto2.id_zona,
            voluntarios=voluntarios,
            estado=dto2.estado,
            fecha_evento=dto2.fecha_evento,
            descripcion=dto2.descripcion
        )
    
    def toEntity(self) -> BatidaEntity:
        return BatidaEntity(
            id=self.id_batida,
            nombre=self.nombre,
            latitud=self.latitud,
            longitud=self.longitud,
            id_zona=self.id_zona,
            voluntarios=json.dumps(self.voluntarios) if self.voluntarios else "[]",
            estado=self.estado,
            fecha_evento=self.fecha_evento,
            descripcion=self.descripcion
        )

class BatidaDTO2(BaseModel):
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
    def fromEntity(cls, entidad: BatidaEntity) -> BatidaDto:
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
    
    def toEntity(self) -> BatidaEntity:
        return BatidaEntity(
            id=self.id_batida,
            nombre=self.nombre,
            latitud=self.latitud,
            longitud=self.longitud,
            id_zona=self.id_zona,
            voluntarios=self.voluntarios,
            estado=self.estado,
            fecha_evento=self.fecha_evento,
            descripcion=self.descripcion
        )