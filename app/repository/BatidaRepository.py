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



