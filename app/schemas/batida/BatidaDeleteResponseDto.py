from pydantic import BaseModel, Field

class EliminarBatidaResponseDto(BaseModel):
    id_batida: int = Field(..., description="ID de la batida eliminada")
    message: str = Field("Batida eliminada exitosamente", description="Mensaje de confirmación de la eliminación")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"id_batida": 10, "message": "Batida eliminada exitosamente"}
            ]
        }
    }
