from pydantic import BaseModel, Field
from typing import Optional

class VoluntarioNoApuntadoResponse(BaseModel):
    code: int = Field(40020, description="Código específico para voluntario no apuntado")
    message: str = Field(..., description="Mensaje indicando que el voluntario no está apuntado en la batida")
    details: Optional[str] = Field(None, description="Detalles adicionales (ID o contexto)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 40020,
                    "message": "El voluntario V123 no está apuntado a la batida.",
                    "details": "No existe el código en la lista de voluntarios."
                }
            ]
        }
    }

class DesapuntarseResponseDto(BaseModel):
    id_batida: int = Field(..., description="ID de la batida")
    codigo_voluntario: str = Field(..., description="Código del voluntario desapuntado")
    message: str = Field("Voluntario desapuntado exitosamente", description="Mensaje de confirmación")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id_batida": 5,
                    "codigo_voluntario": "V123",
                    "message": "Voluntario desapuntado exitosamente"
                }
            ]
        }
    }

