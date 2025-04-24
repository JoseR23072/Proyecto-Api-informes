# services/BatidaService.py

from schemas.Batida import BatidaDto
from repository.BatidaRepository import BatidaRepository
from fastapi import Depends

class BatidaService:
    def __init__(self, repository: BatidaRepository = Depends()):
        self.repository = repository

    def crear_batida(self, batida_dto: BatidaDto) -> BatidaDto:
        # Convertimos el DTO en entidad para guardarlo
        entidad_batida = batida_dto.toEntity()
        entidad_creada = self.repository.crear_batida(entidad_batida)
        return BatidaDto.fromEntity(entidad_creada)

    def ver_batida(self, id_batida: int):
        
        return None

    def ver_batidas(self):
        # A implementar
        return None

    def modificar_batida(self):
        # A implementar
        return None

    def apuntarse(self):
        # A implementar
        return None

    def desapuntarse(self):
        # A implementar
        return None

    def comprobar_voluntario(self):
        # A implementar
        return None
