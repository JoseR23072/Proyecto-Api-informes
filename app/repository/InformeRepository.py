from models.Voluntario import VoluntarioEntity
from config.database import get_session

def guardar_voluntario(voluntario:VoluntarioEntity):
    with get_session() as session:
        session.add(voluntario)
        session.commit()
        session.refresh(voluntario)
        return voluntario
