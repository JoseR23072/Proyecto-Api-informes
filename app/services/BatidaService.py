# services/BatidaService.py
import ast
from schemas.Batida import BatidaDto,BatidaDTO2
from schemas.batida.BatidaDTO import BatidaDTO
from schemas.batida.BatidaUpdateDto import BatidaUpdateDto
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

    async def crear_batida(self, batida_dto: BatidaCreateDto) -> BatidaResponseDto:
        #Validamos que la id de la zona existe
        zona = await MicroserviciosService.obtener_datos_zona(batida_dto.id_zona)
        if not zona:
            raise ValueError("La zona con el ID proporcionado no existe.")
        
        entidad_batida = batida_dto.to_entity()
        entidad_creada = self.repository.crear_batida(entidad_batida)
        return BatidaResponseDto.from_entity(entidad_creada, [])

    async def ver_batida(self, id_batida: int) -> BatidaResponseDto:
        entidad = self.repository.buscar_batida(id_batida)
        if not entidad:
            raise ValueError("La batida con el ID proporcionado no existe.")
        
        lista_voluntarios = ast.literal_eval(entidad.voluntarios) if entidad.voluntarios else []
        ######### FALTA OBTENER INFORMACION DE LA ZONA
        obtener_info_voluntarios = await MicroserviciosService.obtener_datos_voluntarios(lista_voluntarios)
        
        return BatidaResponseDto.from_entity(entidad,obtener_info_voluntarios)

    async def ver_batidas(self) -> List[BatidaResponseDto]:
        ###FALTA ZONAS
        entidades = self.repository.ver_batidas()
        if not entidades:
            return []

        lista_dto=[BatidaDTO.fromEntity(entidad) for entidad in entidades]
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
        print(voluntario_map)
        lista_batidas=[]
        for b in lista_dto:
            voluntarios_list = ast.literal_eval(b.voluntarios)
            lista_info_voluntarios=[voluntario_map.get(vol_id) for vol_id in voluntarios_list]
            response = BatidaResponseDto(
                id_batida=b.id_batida,
                nombre=b.nombre,
                latitud=b.latitud,
                longitud=b.longitud,
                id_zona=b.id_zona,
                voluntarios=lista_info_voluntarios,
                estado=b.estado,
                fecha_evento=b.fecha_evento,
                descripcion=b.descripcion
            )
            lista_batidas.append(response)
    
        return lista_batidas

    async def modificar_batida(self,dto:BatidaUpdateDto):
        # 1) Verificar que la batida existe
        entidad = self.repository.buscar_batida(dto.id_batida)
        if not entidad:
            raise ValueError(f"La batida con ID {dto.id_batida} no existe.")

        # 2) Validar zona si viene modificada
        if dto.id_zona is not None:
            zona = await MicroserviciosService.obtener_datos_zona(dto.id_zona)
            if not zona:
                raise ValueError(f"La zona con ID {dto.id_zona} no existe.")

        # 3) Validar lista de voluntarios si se envía
        if dto.voluntarios is not None:
            info_vols = await MicroserviciosService.obtener_datos_voluntarios(dto.voluntarios)
            if len(info_vols) != len(dto.voluntarios):
                raise ValueError("Alguno de los IDs de voluntario no existe.")

            # Guardamos la lista serializada
            entidad.voluntarios = json.dumps(dto.voluntarios)

        # 4) Aplicar cambios parciales (solo los campos no None)
        for field, value in dto.model_dump().items():
            if field == "id_batida" or value is None:
                continue
            setattr(entidad, field, value)

        # 5) Persistir
        entidad_modificada = self.repository.modificar_batida(entidad)

        # 6) Convertir lista de voluntarios al objeto DTO
        lista_ids = json.loads(entidad_modificada.voluntarios or "[]")
        info_vols_final = await MicroserviciosService.obtener_datos_voluntarios(lista_ids)

        return BatidaResponseDto.from_entity(entidad_modificada, info_vols_final)

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
        
