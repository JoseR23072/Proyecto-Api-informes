from pydantic import BaseModel, Field

class BatidasVoluntarioRequestDto(BaseModel):
    voluntariosbatida: str = Field(..., description="Código del voluntario para filtrar batidas")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"voluntariosbatida": "V123"}
            ]
        }
    }