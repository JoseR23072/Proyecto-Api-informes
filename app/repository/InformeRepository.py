from models.Voluntario import Voluntario
from config.database import get_session

def guardar_voluntario(voluntario_data):
    with get_session() as session:
        voluntario = Voluntario(**voluntario_data.dict())
        session.add(voluntario)
        session.commit()
        session.refresh(voluntario)
        return voluntario
