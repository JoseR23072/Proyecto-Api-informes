from pydantic import BaseModel, Field
from typing import List
from datetime import date
from schemas.Voluntario import VoluntarioDto
from models.Batida import BatidaEntity
from schemas.Zona import ZonaDto
class BatidaZonaResponseDto(BaseModel):
    id: int = Field(..., description="ID generado de la batida")
    nombre: str = Field(..., description="Nombre de la batida")
    latitud: float = Field(..., description="Latitud de la ubicación")
    longitud: float = Field(..., description="Longitud de la ubicación")
    voluntariosbatida : str = Field(..., description="Lista de los nombres de voluntarios")
    estado: bool = Field(..., description="Estado de la batida")
    fecha: date = Field(..., description="Fecha del evento")
    descripcion: str = Field(..., description="Descripción de la batida")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id_batida": 1,
                    "nombre": "Batida en el Parque Natural",
                    "latitud": 40.4168,
                    "longitud": -3.7038,
                    "voluntariosbatida": "Ana Maria Hernandez, Miguel Coquin Hernandez",
                    "estado": False,
                    "fecha_evento": "2025-04-26",
                    "descripcion": "Batida de limpieza y reforestación"
                }
            ]
        }
    }

    @classmethod
    def from_entity(cls, entidad: BatidaEntity,voluntarios: str) -> "BatidaZonaResponseDto":
        """
        Convierte una entidad BatidaEntity en un BatidaResponseDto, usando una lista de VoluntarioDto.
        """
        return cls(
            id=entidad.id,
            nombre=entidad.nombre,
            latitud=entidad.latitud,
            longitud=entidad.longitud,
            voluntariosbatida=voluntarios,
            estado=entidad.estado,
            fecha=entidad.fecha_evento,
            descripcion=entidad.descripcion,
        )
    