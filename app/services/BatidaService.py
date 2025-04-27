# services/BatidaService.py
import ast
from schemas.Batida import BatidaDto,BatidaDTO2
from schemas.Voluntario import VoluntarioDto

from schemas.batida.BatidaCreateDto import BatidaCreateDto
from schemas.batida.BatidaResponseDto import BatidaResponseDto


from repository.BatidaRepository import BatidaRepository
from fastapi import Depends
import asyncio
from services.MicroserviciosService import MicroserviciosService
from typing import List,Dict
import json
class BatidaService:
    def __init__(self, repository: BatidaRepository = Depends()):
        self.repository = repository

    def crear_batida(self, batida_dto: BatidaCreateDto) -> BatidaResponseDto:
        # Convertimos el DTO en entidad para guardarlo
        entidad_batida = batida_dto.to_entity()
        entidad_creada = self.repository.crear_batida(entidad_batida)

        return BatidaResponseDto.from_entity(entidad_creada,[])

    async def ver_batida(self, id_batida: int) -> BatidaDto:
        entidad=self.repository.buscar_batida(id_batida)

        lista_voluntarios = ast.literal_eval(entidad.voluntarios) if entidad.voluntarios else []
        print(lista_voluntarios)
        obtener_info_voluntarios = await MicroserviciosService.obtener_datos_voluntarios(lista_voluntarios)

        entidad.voluntarios=obtener_info_voluntarios
        
        return BatidaDto.fromEntity(entidad)

    async def ver_batidas(self) -> List[BatidaDto]:
        entidades = self.repository.ver_batidas()
        if not entidades:
            return []

        lista_dto=[BatidaDTO2.fromEntity(entidad) for entidad in entidades]
        #se crea un set para que no se repitan los ids
        all_ids = set()
        for b in lista_dto:
            lista_voluntarios=ast.literal_eval(b.voluntarios)
            all_ids.update(lista_voluntarios)

        voluntarios_info = await MicroserviciosService.obtener_datos_voluntarios(list(all_ids))

        # 5. Indexar por número de voluntario para acceso rápido
        voluntario_map: Dict[str, VoluntarioDto] = {
            v.numerovoluntario: v for v in voluntarios_info
        }

        lista_batidas=[]
        for b in lista_dto:
            print("hola mundo")
            voluntarios_list = ast.literal_eval(b.voluntarios)
            lista_info_voluntarios=[voluntario_map.get(vol_id) for vol_id in voluntarios_list]
            batida_dto = BatidaDto.from_dto2(b, lista_info_voluntarios)
            lista_batidas.append(batida_dto)
    
        return lista_batidas

    def modificar_batida(self,batida:BatidaDTO2):
        entidad=BatidaDTO2.toEntity(batida)
        entidad=self.repository.modificar_batida(entidad)
        return BatidaDTO2.fromEntity(entidad)

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


    def desapuntarse(self,id_batida:int,codigo_voluntario:str):
        batida = self.repository.buscar_batida(id_batida)

        if not batida:
            raise ValueError("Batida no encontrada")

        # Convertir el string a lista real de Python usando `ast.literal_eval` (más seguro que eval)
        lista_voluntarios = ast.literal_eval(batida.voluntarios) if batida.voluntarios else []

        if codigo_voluntario not in lista_voluntarios:
            raise ValueError("El voluntario no está apuntado")
        
        lista_voluntarios.remove(codigo_voluntario)

        # Guardar los cambios como string
        batida.voluntarios = str(lista_voluntarios)

        self.repository.actualizar_voluntarios(id_batida,batida.voluntarios)
        return "El voluntario se ha desapuntado correctamente"

    def comprobar_voluntario(self,id_batida:int,codigo_voluntario:str):
        
        batida=self.repository.buscar_batida(id_batida)

        lista_voluntarios=ast.literal_eval(batida.voluntarios) if batida.voluntarios else []

        if codigo_voluntario not in lista_voluntarios:
            return "El voluntario no esta apuntado en esta batida"
        
        else:
            return "El voluntario esta apuntado en esta batida"

    def eliminar_batida(self,id_batida:int):
        respuesta=self.repository.eliminar_batida(id_batida)
        if respuesta:
            return respuesta
        
        else:
            raise ValueError("Batida no encontrada")
        
