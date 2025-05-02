from fastapi import Depends
from typing import List
import asyncio
from datetime import date,datetime
from schemas.batida.BatidaResponseDto import BatidaResponseDto
from services.BatidaService import BatidaService
from utils.enviar_recordatorios_asistencia_batidas import enviar_recordatorios_diarios
from schemas.Voluntario import VoluntarioDto
from utils.enviar_emails import enviar_email_bienvenida

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

    