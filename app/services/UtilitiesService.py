from fastapi import Depends
from typing import List
import asyncio
from datetime import date,timedelta
from schemas.batida.BatidaResponseDto import BatidaResponseDto
from services.BatidaService import BatidaService
from utils.enviar_recordatorios_asistencia_batidas import enviar_recordatorios_diarios
from schemas.Voluntario import VoluntarioDto
from utils.enviar_emails import enviar_email_bienvenida
from repository.BatidaRepository import BatidaRepository
# services/BatidaService.py

from schemas.Voluntario import VoluntarioDto
from schemas.batida.BatidaResponseDto import BatidaResponseDto
from repository.BatidaRepository import BatidaRepository
from fastapi import Depends
from datetime import date
from services.MicroserviciosService import MicroserviciosService
from typing import List,Dict
from models.Batida import BatidaEntity
import ast

class UtilitiesService:
    def __init__(self, repository: BatidaRepository = Depends()):
        self.repository = repository


    """ async def enviar_recordatorios_batidas(self) -> None:
        
        next_day = date.today() + timedelta(days=1)
        # Llamas a tu método nuevo
        batidas_del_proximo_dia: List[BatidaResponseDto] = await self.buscar_batidas_por_fecha(next_day)

        await enviar_recordatorios_diarios(batidas_del_proximo_dia)
 """

   



    async def enviar_recordatorio_manual(self,batida:BatidaResponseDto):

        await enviar_recordatorios_diarios([batida])


    """ async def buscar_batidas_por_fecha(self,fecha:date) -> List[BatidaResponseDto]:
        entidades:List[BatidaEntity]=self.repository.buscar_batidas_por_fecha(fecha)
        
        id_batidas = [e.id for e in entidades]
        all_ids = self.repository.obtener_voluntarios_distintos(id_batidas)

        voluntarios_info = await MicroserviciosService.obtener_datos_voluntarios(all_ids)

        voluntario_map: Dict[int,VoluntarioDto]={
            vol.id:vol for vol in voluntarios_info
        }
        
        lista_completa:List[BatidaResponseDto]=[]

        for ent in entidades:
            lista_ids = self.repository.obtener_voluntarios_por_batida(ent.id)

            lista_info_voluntarios= [voluntario_map[id] for id in lista_ids if id in voluntario_map]

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

        return lista_completa """

    async def enviar_email_codigo_voluntario(self, voluntario: VoluntarioDto) -> None:
        """
        Envía el email de bienvenida / asignación de código al voluntario.
        """
        loop = asyncio.get_running_loop()

        try:
            
            await loop.run_in_executor(
                None,
                enviar_email_bienvenida,
                voluntario
            )
        except Exception as e:
            # aquí podrías mapear a HTTPException o loggear
            raise RuntimeError(f"No se pudo enviar código al voluntario: {e}")

    