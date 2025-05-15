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

    