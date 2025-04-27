# services/BatidaService.py
import ast
from schemas.Voluntario import VoluntarioDto
from fastapi import Depends
import asyncio
from services.MicroserviciosService import MicroserviciosService
from typing import List,Dict
import json
class BatidaService:
    
    def generar_informe(self, zona_id: int) :
        return None


