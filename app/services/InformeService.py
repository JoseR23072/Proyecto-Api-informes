# services/BatidaService.py
from fastapi import Depends
from typing import Literal
from utils.generar_pdf_informe_batida import generar_pdf
from utils.generar_excel_informe_batida import generar_excel_informe_batida
from schemas.batida.BatidaResponseDto import BatidaResponseDto
from services.BatidaService import BatidaService
from schemas.Zona import ZonaDto
from services.MicroserviciosService import MicroserviciosService
from utils.generar_pdf_informe_zona import generar_pdf_informe_zona
from utils.generar_excel_informe_zona import generar_excel_informe_zona
class InformeService:
    def __init__(self, batida_service: BatidaService = Depends()):
        """
        Inyectamos el servicio de batida
        """
        self.batida_service = batida_service

    async def generar_informe_batida(
        self,
        id_batida: int,
        tipo: Literal["pdf", "excel"]
    ) -> str:
        """
        Genera un informe (PDF o Excel) de los asistentes a la batida indicada.

        Args:
            id_batida (int): ID de la batida.
            tipo (str): 'pdf' o 'excel'.

        Returns:
            str: Ruta al archivo generado.

        Raises:
            ValueError: Si la batida no existe.
        """
        # 1) Obtengo la batida completa (lanza ValueError si no existe)
        batida: BatidaResponseDto = await self.batida_service.ver_batida(id_batida)

        # 2) Generar el informe en el formato solicitado
        if tipo == "pdf":
            ruta = generar_pdf(batida)
        else:  # tipo == "excel"
            ruta = generar_excel_informe_batida(batida)

        return ruta

    async def generar_informe_zona(
        self,
        id_zona: int,
        tipo: Literal["pdf", "excel"]
    ) -> str:
        """
        Genera un informe (PDF o Excel) de los voluntarios en la zona indicada.

        Args:
            id_zona (int): ID de la zona.
            tipo (str): 'pdf' o 'excel'.

        Returns:
            str: Ruta al archivo generado.

        Raises:
            ValueError: Si la zona no existe.
        """
        # 1) Obtengo la zona completa (lanza ValueError si no existe)
        zona: ZonaDto = await MicroserviciosService.obtener_datos_zona(id_zona)

        # 2) Generar el informe en el formato solicitado
        if tipo == "pdf":
            ruta = generar_pdf_informe_zona(zona)
        else:  # tipo == "excel"
            ruta = generar_excel_informe_zona(zona)

        return ruta