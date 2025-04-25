# services/BatidaService.py
import ast
import requests
from schemas.Batida import BatidaDto
from repository.BatidaRepository import BatidaRepository
from fastapi import Depends
import asyncio
from services.MicroserviciosService import MicroserviciosService
from typing import List,Dict

class BatidaService:
    def __init__(self, repository: BatidaRepository = Depends()):
        self.repository = repository

    def crear_batida(self, batida_dto: BatidaDto) -> BatidaDto:
        # Convertimos el DTO en entidad para guardarlo
        entidad_batida = batida_dto.toEntity()
        entidad_creada = self.repository.crear_batida(entidad_batida)
        return BatidaDto.fromEntity(entidad_creada)

    def ver_batida(self, id_batida: int):
        entidad=self.repository.buscar_batida(id_batida)

        return BatidaDto.fromEntity(entidad)

    async def ver_batidas(self) -> List[BatidaDto]:
        entidades = self.repository.ver_batidas()  

        batidas = [BatidaDto.fromEntity(entidad) for entidad in entidades]

        #se crea un set para que no se repitan los ids
        all_ids = set()
        for b in batidas:
            all_ids.update(b.voluntarios or [])

        voluntarios_info = await MicroserviciosService.obtener_datos_voluntarios(list(all_ids))

        # 5. Indexar por número de voluntario para acceso rápido
        voluntario_map: Dict[str, dict] = {
            v.numeroVoluntario: v for v in voluntarios_info
        }

        for b in batidas:
            lista_info_voluntarios=[voluntario_map.get(str(vol_id)) for vol_id in (b.voluntarios or [])]
            b.voluntarios=lista_info_voluntarios
        return batidas

    def modificar_batida(self):
        # A implementar
        return None

    async def apuntarse(self,id_batida:int,id_voluntario:str):
        batida = self.repository.buscar_batida(id_batida)

        if not batida:
            raise ValueError("Batida no encontrada")

        # Convertir el string a lista real de Python usando `ast.literal_eval` (más seguro que eval)
        lista_voluntarios = ast.literal_eval(batida.voluntarios) if batida.voluntarios else []

        if id_voluntario in lista_voluntarios:
            raise ValueError("El voluntario ya está apuntado")

        # Agregar el nuevo voluntario
        lista_voluntarios.append(id_voluntario)

        # Guardar los cambios como string
        batida.voluntarios = str(lista_voluntarios)

        actualizar_bdd = asyncio.to_thread(
        self.repository.actualizar_voluntarios, id_batida, batida.voluntarios
    )

        obtener_info_voluntarios = MicroserviciosService.obtener_datos_voluntarios(lista_voluntarios)

        datos_batida, datos_voluntarios = await asyncio.gather(actualizar_bdd, obtener_info_voluntarios)

        return {
        "batida": datos_batida,
        "voluntarios": datos_voluntarios
    }


    def desapuntarse(self):
        # A implementar
        return None

    def comprobar_voluntario(self,id_batida:int,id_voluntario:str):
        
        # A implementar
        return None
