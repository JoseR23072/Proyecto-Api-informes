import logging
import asyncio
from utils.generar_pdf_recordatorio_asistencia_batida import generar_pdf_recordatorio
from utils.enviar_emails import enviar_email_recordatorio
from typing import List
from schemas.batida.BatidaResponseDto import BatidaResponseDto


# Función asíncrona  envío de recordatorios a los voluntarios apuntados a una batida
async def enviar_recordatorios_diarios(batidas:List[BatidaResponseDto]):
    logging.info("Ejecutando tarea programada para enviar recordatorios...")
    logging.info(f"{batidas}")

    for batida in batidas:
        batida_fecha = batida.fecha_evento
        # Comprueba si hoy es exactamente un día antes de la fecha de la batida
        logging.info(f"Se enviarán recordatorios para la batida '{batida.nombre}' programada para {batida_fecha}.")
        
        # Recorrer cada voluntario de la batida y generar el PDF (o enviar correo)
        for voluntario in batida.voluntarios:
                # Llamamos a la función existente que genera el PDF recordatorio para cada voluntario.
                # Nota: Si la función también envía el correo, se invocaría ahí; de lo contrario, aquí se podría invocar una función de envío.
                pdf_path=generar_pdf_recordatorio(
                    nombre_voluntario=voluntario.nombre + " " + voluntario.apellidos,
                    nombre_batida=batida.nombre,
                    fecha=str(batida_fecha),
                    latitud=batida.latitud,
                    longitud=batida.longitud,
                    ciudad="Prueba"
                )
                
                enviar_email_recordatorio(pdf_file_path=pdf_path, destinatario=voluntario.email)
                logging.info(f"Recordatorio generado para {voluntario.email}.")
                
    
        else:
            logging.info(f"No se envía recordatorio para '{batida.nombre}' (fecha programada: {batida_fecha}).")
    
    logging.info("Tarea de recordatorios completada.")

# Para ejecutar la función de forma inmediata (por ejemplo, en pruebas locales):
if __name__ == "__main__":
    # Configura el logging
    logging.basicConfig(level=logging.INFO)
    
    # Ejecuta la función de recordatorios (usamos asyncio.run para llamar a la función asíncrona)
    asyncio.run(enviar_recordatorios_diarios())
