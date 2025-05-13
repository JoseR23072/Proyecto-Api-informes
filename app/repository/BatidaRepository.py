from models.Batida import BatidaEntity
from config.database import get_session
from fastapi import Depends
from sqlmodel import Session,select,delete,distinct
from models.BatidaVoluntario import BatidaVoluntario
from typing import List
from datetime import date


class BatidaRepository:
    def __init__(self, session:Session=Depends(get_session)):
        self.session=session

    def crear_batida(self, batida:BatidaEntity)->BatidaEntity:
        self.session.add(batida)
        self.session.commit()
        self.session.refresh(batida)
        return batida

    def buscar_batida(self,id_batida:int)->BatidaEntity:
        return self.session.get(BatidaEntity,id_batida)

    def ver_batidas(self)->list[BatidaEntity]:
        statement=select(BatidaEntity)
        return self.session.exec(statement)

    def modificar_batida(self, batida: BatidaEntity) -> BatidaEntity:
        batida_existente = self.session.get(BatidaEntity, batida.id)
        if batida_existente:
            batida_existente.nombre = batida.nombre
            batida_existente.latitud = batida.latitud
            batida_existente.longitud = batida.longitud
            batida_existente.id_zona = batida.id_zona
            batida_existente.fecha_evento = batida.fecha_evento
            batida_existente.descripcion = batida.descripcion
            batida_existente.estado = batida.estado

            self.session.commit()
            self.session.refresh(batida_existente)
            return batida_existente
        return None
    
    def apuntar_voluntario(self, id_batida: int, id_voluntario: int) -> None:
        voluntario = BatidaVoluntario(id_batida=id_batida, id_voluntario=id_voluntario)
        self.session.add(voluntario)
        self.session.commit()
    
    def desapuntar_voluntario(self, id_batida: int, id_voluntario: int) -> None:
        self.session.exec(
            delete(BatidaVoluntario).where(
                BatidaVoluntario.id_batida == id_batida,
                BatidaVoluntario.id_voluntario == id_voluntario
            )
        )
        self.session.commit()

    def eliminar_batida(self,id_batida:int) -> bool:
        batida = self.session.get(BatidaEntity, id_batida)
        if batida:
            self.session.delete(batida)
            self.session.commit()
            return True
        return False

    def buscar_batidas_por_fecha(self,fecha:date) -> List[BatidaEntity]:
        statement=select(BatidaEntity).where(BatidaEntity.fecha_evento==fecha)

        resultado=self.session.exec(statement).all()
        return resultado
    
    def buscar_batidas_por_zona(self,id_zona:int)->List[BatidaEntity]:
        statement=select(BatidaEntity).where(BatidaEntity.id_zona==id_zona)
        resultado=self.session.exec(statement).all()
        return resultado
    
    def obtener_voluntarios_por_batida(self, id_batida: int) -> List[int]:
        statement = select(BatidaVoluntario.id_voluntario).where(BatidaVoluntario.id_batida == id_batida)
        resultado = self.session.exec(statement).all()
        return resultado
    
    def obtener_voluntarios_distintos(self, id_batidas: List[int] ) -> List[int]:
        statement = select(distinct(BatidaVoluntario.id_voluntario))
        if id_batidas is not None:
            statement = statement.where(BatidaVoluntario.id_batida.in_(id_batidas))
        resultado = self.session.exec(statement).all()
        return resultado
    
    def modificar_relaciones_voluntarios(self, id_batida: int, nuevos_voluntarios: List[int]) -> None:
        # Eliminar registros existentes
        self.session.exec(
            delete(BatidaVoluntario).where(BatidaVoluntario.id_batida == id_batida)
        )

        # Agregar nuevos registros
        for id_vol in nuevos_voluntarios:
            self.session.add(BatidaVoluntario(id_batida=id_batida, id_voluntario=id_vol))

        self.session.commit()

    def obtener_batidas_por_voluntario(self, id_voluntario: int) -> List[BatidaEntity]:
        statement = (
            select(BatidaEntity)
            .join(BatidaVoluntario, BatidaEntity.id == BatidaVoluntario.id_batida)
            .where(BatidaVoluntario.id_voluntario == id_voluntario)
        )
        return self.session.exec(statement).all()