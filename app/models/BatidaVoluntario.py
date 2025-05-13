from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey,Integer



class BatidaVoluntario(SQLModel, table=True):

    __tablename__ = 'BatidaVoluntario'

    id_batida: int = Field(sa_column=Column(ForeignKey("Batida.id", ondelete="CASCADE"), primary_key=True))
    id_voluntario: int = Field(sa_column=Column(Integer,primary_key=True))