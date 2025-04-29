# schemas/batida/ApuntarseResponseDto.py
from pydantic import BaseModel, Field
from typing import List, Any

class ApuntarseResponseDto(BaseModel):
    id_batida: int = Field(..., description="ID de la batida a la que se ha apuntado el voluntario")
    codigo_voluntario: str = Field(..., description="Código del voluntario apuntado")
    
    message: str = Field(
        "Voluntario apuntado exitosamente", 
        description="Mensaje de confirmación"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id_batida": 5,
                    "codigo_voluntario": "V123",
                    "message": "Voluntario apuntado exitosamente"
                }
            ]
        }
    }
