from pydantic import BaseModel, Field

class BatidasVoluntarioRequestDto(BaseModel):
    codigo_voluntario: str = Field(..., description="Código del voluntario para filtrar batidas")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"codigo_voluntario": "V123"}
            ]
        }
    }