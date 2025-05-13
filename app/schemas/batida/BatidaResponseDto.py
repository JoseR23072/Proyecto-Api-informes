from pydantic import BaseModel, Field,ConfigDict
from typing import List
from datetime import date
from schemas.Voluntario import VoluntarioDto
from models.Batida import BatidaEntity
from schemas.Zona import ZonaDto
class BatidaResponseDto(BaseModel):
    id_batida: int = Field(..., description="ID generado de la batida")
    nombre: str = Field(..., description="Nombre de la batida")
    latitud: float = Field(..., description="Latitud de la ubicación")
    longitud: float = Field(..., description="Longitud de la ubicación")
    zona: ZonaDto = Field(..., description="ID de la zona asociada")
    voluntarios: List[VoluntarioDto] = Field(..., description="Lista de los voluntarios")
    estado: bool = Field(..., description="Estado de la batida")
    fecha_evento: date = Field(..., description="Fecha del evento")
    descripcion: str = Field(..., description="Descripción de la batida")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id_batida": 1,
                    "nombre": "Batida en el Parque Natural",
                    "latitud": 40.4168,
                    "longitud": -3.7038,
                    "id_zona": 2,
                    "voluntarios": [
                    ],
                    "estado": False,
                    "fecha_evento": "2025-04-26",
                    "descripcion": "Batida de limpieza y reforestación"
                }
            ]
        }
    )
    

    @classmethod
    def from_entity(cls, entidad: BatidaEntity, voluntarios: List[VoluntarioDto],zona:ZonaDto) -> "BatidaResponseDto":
        """
        Convierte una entidad BatidaEntity en un BatidaResponseDto, usando una lista de VoluntarioDto.
        """
        return cls(
            id_batida=entidad.id,
            nombre=entidad.nombre,
            latitud=entidad.latitud,
            longitud=entidad.longitud,
            voluntarios=voluntarios,
            estado=entidad.estado,
            fecha_evento=entidad.fecha_evento,
            descripcion=entidad.descripcion,
            zona=zona
        )
    
class BatidaGetResponseDto(BatidaResponseDto):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id_batida": 1,
                    "nombre": "Batida en el Parque Natural",
                    "latitud": 40.4168,
                    "longitud": -3.7038,
                    "id_zona": 2,
                    "voluntarios": [
                        {
      "id": 1,
      "nombre": "Ana",
      "apellidos": "Maria Hernandez",
      "email": "AnaMariaHernandez@example.com",
      "dni": "123456K",
      "numerovoluntario": "Mi123456789",
      "rol": "voluntario"
    },
    {
      "id": 2,
      "nombre": "Miguel",
      "apellidos": "Fernandez",
      "email": "mg@example.com",
      "dni": "123456K",
      "numerovoluntario": "IM123456789",
      "rol": "voluntario"
    }
                    ],
                    "estado": False,
                    "fecha_evento": "2025-04-26",
                    "descripcion": "Batida de limpieza y reforestación"
                }
            ]
        }
    }
