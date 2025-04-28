from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from models.Batida import BatidaEntity  # Asumimos que esta es tu entidad

class BatidaCreateDto(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre de la batida")
    latitud: float = Field(..., ge=-90, le=90, description="Latitud de la ubicación")
    longitud: float = Field(..., ge=-180, le=180, description="Longitud de la ubicación")
    id_zona: int = Field(..., gt=0, description="ID de la zona asociada")
    fecha_evento: date = Field(..., description="Fecha del evento")
    descripcion: str = Field(..., min_length=1, description="Descripción de la batida")
    estado: Optional[bool] = Field(default=False, description="Estado de la batida (activa/inactiva)")
    

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Batida en el Parque Natural",
                    "latitud": 40.4168,
                    "longitud": -3.7038,
                    "id_zona": 2,
                    "fecha_evento": "2025-04-26",
                    "descripcion": "Batida de limpieza y reforestación",
                    "estado": False,
                }
            ]
        }
    }

    def to_entity(self) -> BatidaEntity:
        """
        Convierte el DTO a una entidad BatidaEntity, transformando la lista de voluntarios a una cadena JSON.
        """
        return BatidaEntity(
            nombre=self.nombre,
            latitud=self.latitud,
            longitud=self.longitud,
            id_zona=self.id_zona,
            fecha_evento=self.fecha_evento,
            descripcion=self.descripcion,
            estado=self.estado,
            voluntarios="[]"
        )