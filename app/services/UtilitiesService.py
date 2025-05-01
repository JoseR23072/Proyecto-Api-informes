from fastapi import Depends
from typing import List
from datetime import date,datetime
from schemas.batida.BatidaResponseDto import BatidaResponseDto
from services.BatidaService import BatidaService
from utils.enviar_recordatorios_asistencia_batidas import enviar_recordatorios_diarios


class UtilitiesService:
    def __init__(self, batida_service: BatidaService = Depends()):
        self.batida_service = batida_service

    async def enviar_recordatorios_batidas(self) -> None:
        
        next_day = date.today() + datetime.timedelta(days=1)
        # Llamas a tu método nuevo
        batidas_del_proximo_dia: List[BatidaResponseDto] = await self.batida_service.buscar_batidas_por_fecha(next_day)

        await enviar_recordatorios_diarios(batidas_del_proximo_dia)

    async def enviar_recordatorio_manual(self,batida:BatidaResponseDto):

        await enviar_recordatorios_diarios([batida])