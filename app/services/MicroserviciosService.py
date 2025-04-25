from settings import settings  # si usas Pydantic
from schemas.Voluntario import VoluntarioDto
from typing import List
import httpx
class MicroserviciosService:
    @staticmethod
    async def obtener_datos_voluntarios(ids: List[str]) -> List[VoluntarioDto]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.VOLUNTARIOS_API_URL}/info",
                params={"ids": ",".join(ids)}
            )
            response.raise_for_status()
            return [VoluntarioDto(**v) for v in response.json()]
