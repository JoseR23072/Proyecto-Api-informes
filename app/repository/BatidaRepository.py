from models.Batida import BatidaEntity
from config.database import get_session
from fastapi import Depends
from sqlmodel import Session,select



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

    def modificar_batida(self,batida:BatidaEntity)->BatidaEntity:
        batida_existente = self.session.get(BatidaEntity, batida.id)
        if batida_existente:
            batida_existente.nombre = batida.nombre
            batida_existente.latitud = batida.latitud
            batida_existente.longitud = batida.longitud
            batida_existente.id_zona = batida.id_zona
            batida_existente.voluntarios = batida.voluntarios
            batida_existente.fecha_evento = batida.fecha_evento
            batida_existente.descripcion = batida.descripcion
            batida_existente.estado = batida.estado
            self.session.commit()
            self.session.refresh(batida_existente)
            return batida_existente
        else:
            return None
    
    def actualizar_voluntarios(self, id_batida:int, lista_voluntarios:str):
        batida=self.session.get(BatidaEntity,id_batida)
        if batida:
            batida.voluntarios=lista_voluntarios

            self.session.commit()
            self.session.refresh(batida)
            return batida

        return None
  
    def eliminar_batida(self,id_batida:int) -> bool:
        batida = self.session.get(BatidaEntity, id_batida)
        if batida:
            self.session.delete(batida)
            self.session.commit()
            return True
        return False
