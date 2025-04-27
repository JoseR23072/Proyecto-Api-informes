from config.settings import settings  # si usas Pydantic
from schemas.Voluntario import VoluntarioDto
from schemas.Zona import ZonaDto
from typing import List
import httpx
import asyncio  # Lo necesitas para lanzar la corrutina

class MicroserviciosService:
    @staticmethod
    async def obtener_datos_voluntarios(ids: List[str]) -> List[VoluntarioDto]:
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.MICROSERVICIOS_URL}/voluntarios/verVoluntariosNum",
                params={"ids": ",".join(ids)}
            )
            response.raise_for_status()
            data = response.json()
            if not data:
                return []

            return [VoluntarioDto(**v) for v in data]

    @staticmethod
    async def obtener_datos_zona(id_zona:int) -> ZonaDto:
        async with httpx.AsyncClient() as client:
            response = await client.get(

            )
            return []
        
        
if __name__ == "__main__":
    async def main():
        ids = ["Mi709629567","Mi70962956"]  # ids de ejemplo
        voluntarios = await MicroserviciosService.obtener_datos_voluntarios(ids)
        print(voluntarios)

    asyncio.run(main())