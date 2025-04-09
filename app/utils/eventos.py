import datetime
import logging
import asyncio

# Suponiendo que ya tienes la función existente para generar el PDF recordatorio.
# Por ejemplo, desde tu módulo recordatorio:
from recordatorio import generar_pdf_recordatorio
from correo import enviar_email

# Simulación de datos: función que "consulta" la base de datos y devuelve batidas.
def query_batidas_proximas():
    """
    Simula la consulta de batidas a la base de datos.
    Devuelve una lista de batidas, cada una representada como un diccionario.
    """
    today = datetime.date.today()
    # Batida 1: programada para mañana (recordatorio se envía hoy, 1 día antes)
    batida1 = {
       "nombre_batida": "Batida Playa del Faro",
       "fecha": today + datetime.timedelta(days=1),
       "latitud": 36.7213,
       "longitud": -4.4214,
       "ciudad": "Málaga",
       "voluntarios": [
            {"nombre": "Ana", "apellidos": "Martínez", "email": "maria@example.com"},
            {"nombre": "Juan", "apellidos": "González", "email": "juan@example.com"},
       ]
    }
    # Batida 2: programada para dentro de tres días (no se envía recordatorio hoy)
    batida2 = {
       "nombre_batida": "Batida Río Espejo",
       "fecha": today + datetime.timedelta(days=3),
       "latitud": 37.0,
       "longitud": -4.0,
       "ciudad": "Granada",
       "voluntarios": [
            {"nombre": "Pedro", "apellidos": "Sánchez", "email": "pedro@example.com"},
       ]
    }
    return [batida1, batida2]

# Función asíncrona que simula el envío de recordatorios diarios
async def enviar_recordatorios_diarios():
    logging.info("Ejecutando tarea programada para enviar recordatorios...")
    batidas = query_batidas_proximas()
    today = datetime.date.today()
    
    for batida in batidas:
        batida_fecha = batida["fecha"]
        # Comprueba si hoy es exactamente un día antes de la fecha de la batida
        if today == batida_fecha - datetime.timedelta(days=1):
            logging.info(f"Se enviarán recordatorios para la batida '{batida['nombre_batida']}' programada para {batida_fecha}.")
            # Recorrer cada voluntario de la batida y generar el PDF (o enviar correo)
            for voluntario in batida["voluntarios"]:
                # Llamamos a la función existente que genera el PDF recordatorio para cada voluntario.
                # Nota: Si la función también envía el correo, se invocaría ahí; de lo contrario, aquí se podría invocar una función de envío.
                pdf_path=generar_pdf_recordatorio(
                    nombre_voluntario=voluntario["nombre"] + " " + voluntario["apellidos"],
                    nombre_batida=batida["nombre_batida"],
                    fecha=str(batida_fecha),
                    latitud=batida["latitud"],
                    longitud=batida["longitud"],
                    ciudad=batida["ciudad"]
                )
                enviar_email(pdf_file_path=pdf_path, destinatario=voluntario["email"])
                logging.info(f"Recordatorio generado para {voluntario['email']}.")

        else:
            logging.info(f"No se envía recordatorio para '{batida['nombre_batida']}' (fecha programada: {batida_fecha}).")
    
    logging.info("Tarea de recordatorios completada.")

# Para ejecutar la función de forma inmediata (por ejemplo, en pruebas locales):
if __name__ == "__main__":
    # Configura el logging
    logging.basicConfig(level=logging.INFO)
    
    # Ejecuta la función de recordatorios (usamos asyncio.run para llamar a la función asíncrona)
    asyncio.run(enviar_recordatorios_diarios())
