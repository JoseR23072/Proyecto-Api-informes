# services/BatidaService.py
import ast
import logging
from schemas.batida.BatidaDTO import BatidaDTO
from schemas.batida.BatidaUpdateDto import BatidaUpdateDto
from schemas.Voluntario import VoluntarioDto
from schemas.batida.BatidaDesapuntarseResponseDto import DesapuntarseResponseDto
from schemas.batida.BatidaCreateDto import BatidaCreateDto
from schemas.batida.BatidaResponseDto import BatidaResponseDto
from schemas.batida.ApuntarseResponseDto import ApuntarseResponseDto
from schemas.batida.BatidasVoluntarioRequestDto import BatidasVoluntarioRequestDto
from schemas.batida.BatidaZonaResponseDto import BatidaZonaResponseDto
from schemas.batida.BatidaDeleteResponseDto import EliminarBatidaResponseDto
from repository.BatidaRepository import BatidaRepository
from models.Batida import BatidaEntity
from fastapi import Depends
from datetime import date
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
        return BatidaResponseDto.from_entity(entidad_creada, [],zona)

    async def ver_batida(self, id_batida: int) -> BatidaResponseDto:
        entidad = self.repository.buscar_batida(id_batida)
        if not entidad:
            raise ValueError("La batida con el ID proporcionado no existe.")
        zona = await MicroserviciosService.obtener_datos_zona(entidad.id_zona)
        if not zona:
            raise ValueError("La zona con el ID proporcionado no existe.")
        lista_voluntarios = ast.literal_eval(entidad.voluntarios) if entidad.voluntarios else []
        
        obtener_info_voluntarios = await MicroserviciosService.obtener_datos_voluntarios(lista_voluntarios)
        
        return BatidaResponseDto.from_entity(entidad,obtener_info_voluntarios,zona)

    async def ver_batidas(self) -> List[BatidaResponseDto]:
       
        try:
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
            lista_batidas: List[BatidaResponseDto]=[]
            for b in lista_dto:
                voluntarios_list = ast.literal_eval(b.voluntarios)
                lista_info_voluntarios=[voluntario_map[vol_id] for vol_id in voluntarios_list if vol_id in voluntario_map]
                zona = await MicroserviciosService.obtener_datos_zona(b.id_zona)
                response = BatidaResponseDto(
                    id_batida=b.id_batida,
                    nombre=b.nombre,
                    latitud=b.latitud,
                    longitud=b.longitud,
                    zona=zona,
                    voluntarios=lista_info_voluntarios,
                    estado=b.estado,
                    fecha_evento=b.fecha_evento,
                    descripcion=b.descripcion
                )
                lista_batidas.append(response)
        
            return lista_batidas
        except Exception as e:
            logging.exception("Error inesperado en ver_batidas")
            raise e
    async def modificar_batida(self,dto:BatidaUpdateDto)->BatidaResponseDto:
       #verificamos que la batida existe
        entidad = self.repository.buscar_batida(dto.id_batida)
        if not entidad:
            raise ValueError(f"La batida con ID {dto.id_batida} no existe.")

        # Validar zona si se modifica
        if dto.id_zona is not None:
            zona = await MicroserviciosService.obtener_datos_zona(dto.id_zona)
            if not zona:
                raise ValueError(f"La zona con ID {dto.id_zona} no existe.")


        # validamos que la lista de voluntarios no contenga ids incorrectos
        if dto.voluntarios is not None:
            voluntarios=ast.literal_eval(dto.voluntarios)
            info_vols = await MicroserviciosService.obtener_datos_voluntarios(voluntarios)
            
            if len(info_vols) != len(voluntarios):
                raise ValueError("Alguno de los IDs de voluntario no existe.")

            # Guardamos la lista serializada
            entidad.voluntarios = str(dto.voluntarios)

        #modificamos unicamente los campos que no sean None
        for field, value in dto.model_dump().items():
            if field == "id_batida" or value is None:
                continue
            setattr(entidad, field, value)

        
        entidad_modificada = self.repository.modificar_batida(entidad)

        lista_ids = json.loads(entidad_modificada.voluntarios or "[]")
        info_vols_final = await MicroserviciosService.obtener_datos_voluntarios(lista_ids)

        return BatidaResponseDto.from_entity(entidad_modificada, info_vols_final,zona)

    async def apuntarse(self,id_batida:int,codigo_voluntario:str) -> ApuntarseResponseDto:
        entidad = self.repository.buscar_batida(id_batida)

        if not entidad:
            raise ValueError(f"La batida con ID {id_batida} no existe.")

         # Validar existencia del voluntario en el microservicio
        voluntario = await MicroserviciosService.obtener_datos_voluntario(codigo_voluntario)
        if not voluntario:
            raise ValueError(f"El voluntario con código {codigo_voluntario} no existe.")

        # Convertir el string a lista real de Python 
        lista_voluntarios = ast.literal_eval(entidad.voluntarios) if entidad.voluntarios else []


        if codigo_voluntario in lista_voluntarios:
            raise ValueError(f"El voluntario {codigo_voluntario} ya está apuntado a la batida.")
                
        lista_voluntarios.append(codigo_voluntario)

        

        self.repository.actualizar_voluntarios(id_batida,str(lista_voluntarios))

        return ApuntarseResponseDto(
            id_batida=id_batida,
            codigo_voluntario=codigo_voluntario,
            message="Voluntario apuntado exitosamente"
        )


    async def desapuntarse(self,id_batida:int,codigo_voluntario:str) -> DesapuntarseResponseDto:
        entidad = self.repository.buscar_batida(id_batida)

        if not entidad:
            raise ValueError(f"La batida con ID {id_batida} no existe.")

         # Validar existencia del voluntario en el microservicio
        voluntario = await MicroserviciosService.obtener_datos_voluntario(codigo_voluntario)
        if not voluntario:
            raise ValueError(f"El voluntario con código {codigo_voluntario} no existe.")

        # Convertir el string a lista real de Python 
        lista_voluntarios = ast.literal_eval(entidad.voluntarios) if entidad.voluntarios else []


        if codigo_voluntario not in lista_voluntarios:
            raise ValueError(f"El voluntario {codigo_voluntario} no estaba apuntado a la batida.")
                
        lista_voluntarios.remove(codigo_voluntario)

        

        self.repository.actualizar_voluntarios(id_batida,str(lista_voluntarios))

        return DesapuntarseResponseDto(
            id_batida=id_batida,
            codigo_voluntario=codigo_voluntario,
            message="Voluntario desapuntado exitosamente"
        )



    async def ver_batidas_por_voluntario(self, dto: BatidasVoluntarioRequestDto) -> List[BatidaResponseDto]:
        #Validar si el voluntario existe
        voluntario = await MicroserviciosService.obtener_datos_voluntario(dto.voluntariosbatida)
        if not voluntario:
            raise ValueError(f"El voluntario con código {dto.voluntariosbatida} no existe.")

        # Obtener todas las batidas y filtrar por código
        entidades = self.repository.ver_batidas()
        filtradas: List[BatidaEntity] = []
        for entidad in entidades:
            lista_ids = ast.literal_eval(entidad.voluntarios) if entidad.voluntarios else []
            if dto.voluntariosbatida in lista_ids:
                filtradas.append(entidad)

        if not filtradas:
            return []

        # 3) Recolectar todos los voluntarios de esas batidas para obtener info
        all_ids = set()
        for ent in filtradas:
            ids = ast.literal_eval(ent.voluntarios) if ent.voluntarios else []
            all_ids.update(ids)

        voluntarios_info = await MicroserviciosService.obtener_datos_voluntarios(list(all_ids))
        # map por numerovoluntario
        voluntario_map: Dict[str, VoluntarioDto] = {
            v.numerovoluntario: v for v in voluntarios_info
        }

        # 4) Construir lista de DTOs
        lista_filtrada: List[BatidaResponseDto] = []
        for ent in filtradas:
            voluntarios_list = ast.literal_eval(ent.voluntarios) if ent.voluntarios else []
            lista_info_voluntarios=[voluntario_map.get(vol_id) for vol_id in voluntarios_list if vol_id in voluntario_map]
            
            zona = await MicroserviciosService.obtener_datos_zona(ent.id_zona)
            response = BatidaResponseDto(
                id_batida=ent.id,
                nombre=ent.nombre,
                latitud=ent.latitud,
                longitud=ent.longitud,
                zona=zona,
                voluntarios=lista_info_voluntarios,
                estado=ent.estado,
                fecha_evento=ent.fecha_evento,
                descripcion=ent.descripcion
            )
            lista_filtrada.append(response)
        return lista_filtrada


    def eliminar_batida(self, id_batida: int) -> EliminarBatidaResponseDto:
        entidad = self.repository.buscar_batida(id_batida)
        if not entidad:
            raise ValueError(f"La batida con ID {id_batida} no existe.")

        self.repository.eliminar_batida(id_batida)

        return EliminarBatidaResponseDto(
            id_batida=id_batida,
            message="Batida eliminada exitosamente"
        )
    
    async def buscar_batidas_por_fecha(self,fecha:date) -> List[BatidaResponseDto]:
        entidades:List[BatidaEntity]=self.repository.buscar_batidas_por_fecha(fecha)
        
        all_ids = set()
        for ent in entidades:
            codigos_voluntarios = ast.literal_eval(ent.voluntarios) if ent.voluntarios else []
            all_ids.update(codigos_voluntarios)


        voluntarios_info = await MicroserviciosService.obtener_datos_voluntarios(list(all_ids))

        voluntario_map: Dict[str,VoluntarioDto]={
            vol.numerovoluntario:vol for vol in voluntarios_info
        }
        
        lista_completa:List[BatidaResponseDto]=[]

        for entidad in entidades:
            voluntario_codigos=ast.literal_eval(ent.voluntarios) if ent.voluntarios else []
            lista_info_voluntarios=[voluntario_map.get(vol_id) for vol_id in voluntario_codigos if vol_id in voluntario_map]

            zona = await MicroserviciosService.obtener_datos_zona(ent.id_zona)
            response = BatidaResponseDto(
                id_batida=ent.id,
                nombre=ent.nombre,
                latitud=ent.latitud,
                longitud=ent.longitud,
                zona={},
                voluntarios=lista_info_voluntarios,
                estado=ent.estado,
                fecha_evento=ent.fecha_evento,
                descripcion=ent.descripcion
            )
            lista_completa.append(response)

        return lista_completa
    

    async def buscar_batidas_de_una_zona(self,id_zona:int)-> List[BatidaZonaResponseDto]:
    
        zona = await MicroserviciosService.obtener_datos_zona(id_zona)
        if not zona:
            raise ValueError(f"La zona con ID {id_zona} no existe.")
            
        batidasEntidades=self.repository.buscar_batidas_por_zona(id_zona)

        if not batidasEntidades:
            return [

            ]
        
        ids_voluntarios=set()
        for batida in batidasEntidades:
            vol=ast.literal_eval(batida.voluntarios) if batida.voluntarios else []
            ids_voluntarios.update(vol)
        
        voluntarios_info:List[VoluntarioDto]=await MicroserviciosService.obtener_datos_voluntarios(list(ids_voluntarios))

        voluntarios_map={
            vol.numerovoluntario:""+vol.nombre+vol.apellidos for vol in voluntarios_info 
        }

        lista_batidas:List[BatidaZonaResponseDto]=[]

        for ent in batidasEntidades:
            vol_ids=ast.literal_eval(ent.voluntarios) if ent.voluntarios else []
            lista_info_voluntarios=[
                voluntarios_map.get(vol) for vol in vol_ids if vol in vol_ids
            ]

            nombres_voluntarios = ",".join(lista_info_voluntarios) if lista_info_voluntarios else ""

            ent.voluntarios=nombres_voluntarios
            lista_batidas.append(BatidaZonaResponseDto.from_entity(ent))

        return lista_batidas