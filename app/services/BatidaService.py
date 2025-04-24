# services/BatidaService.py
import ast
import requests
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
        entidad=self.repository.buscar_batida(id_batida)

        return BatidaDto.fromEntity

    def ver_batidas(self):
        # A implementar
        return None

    def modificar_batida(self):
        # A implementar
        return None

    def apuntarse(self,id_batida:int,id_voluntario:str):
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

        self.repository.actualizar_voluntarios(id_batida, str(lista_voluntarios))

        return None
    def desapuntarse(self):
        # A implementar
        return None

    def comprobar_voluntario(self):
        # A implementar
        return None
