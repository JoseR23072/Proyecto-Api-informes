from config.settings import settings  # si usas Pydantic
from schemas.Voluntario import VoluntarioDto
from schemas.Ciudad import CiudadDto
from schemas.Zona import ZonaDto
from typing import List,Optional
import httpx
import asyncio  # Lo necesitas para lanzar la corrutina

class MicroserviciosService:
    @staticmethod
    async def obtener_datos_voluntarios(ids: List[str]) -> List[VoluntarioDto]:
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.MICROSERVICIOS_URL}/voluntarios/verVoluntariosNum",
                params={"numeros": ",".join(ids)}
            )
            response.raise_for_status()
            data = response.json()
            if not data:
                return []

            return [VoluntarioDto(**v) for v in data]

    @staticmethod
    async def obtener_datos_zona(id_zona:int) -> Optional[ZonaDto]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.MICROSERVICIOS_URL}/zonas/verZonaInfo",
                params={"id": id_zona}
            )
            if response.status_code == 500:
                return None
            if response.status_code == 204 or not response.content:
                return None
            data = response.json()
            ciudad = CiudadDto(**data["ciudad"])
            voluntarios = [VoluntarioDto(**vol) for vol in data.get("voluntariosZona", [])]

            
            return ZonaDto(
                id=data["id"],
                nombre=data["nombre"],
                latitud=data["latitud"],
                longitud=data["longitud"],
                ciudad=ciudad,
                voluntariosZona=voluntarios
            )
    @staticmethod
    async def obtener_datos_voluntario(id: str) -> Optional[VoluntarioDto]:
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.MICROSERVICIOS_URL}/voluntarios/verVoluntarioNum",
                json={"numerovoluntario": id}
            )
        if response.status_code == 204 or not response.content:
            return None
        data = response.json()
        
        return VoluntarioDto(**data)
        
if __name__ == "__main__":
    async def main():
        ids = ["Mi709629567","Mi70962956"]  # ids de ejemplo
        voluntarios = await MicroserviciosService.obtener_datos_voluntarios(ids)
        print(voluntarios)

    asyncio.run(main())