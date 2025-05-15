import yagmail
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from config.settings import settings
import logging
from schemas.Voluntario import VoluntarioDto

def enviar_email_recordatorio(pdf_file_path, destinatario,nombre:str):
    logging.info(f"El email es : {settings.EMAIL}")
    logging.info(f"La contraseña del envio del correo es : {settings.EMAIL_PASSWORD}")
    # Autenticación de Gmail
    yag = yagmail.SMTP(user=settings.EMAIL, password=settings.EMAIL_PASSWORD)

    asunto="Recordatorio Batida RiverSpain: ¡Nos encontramos en la acción!"

    
    cuerpo_email = f"""\
Estimado/a {nombre},

Te saludamos desde RiverSpain y queremos recordarte tu participación en nuestra próxima batida. Adjuntamos un archivo PDF con todos los detalles e instrucciones sobre la actividad.

Agradecemos tu compromiso y dedicación para conservar nuestros ríos y océanos, y estamos seguros de que tu participación marcará la diferencia.

Si necesitas más información o tienes alguna duda, no dudes en contactarnos.

¡Nos vemos pronto!

Un cordial saludo,
El equipo de RiverSpain 🌿
"""


    # Enviar el correo con el archivo adjunto
    yag.send(
        to=destinatario,
        subject=asunto,
        contents=cuerpo_email,
        attachments=pdf_file_path
    )

    os.remove(pdf_file_path)

def enviar_email_bienvenida(vol: VoluntarioDto) -> None:
        """
        Envía un email de bienvenida con el número de voluntario incrustado.
        """
        try:
            directorio_actual = Path(__file__).parent  
            # Esto será /app/utils

            directorio_archivos = directorio_actual / "envio_codigo_voluntario"

            logo_path=directorio_archivos / "logo.png"

            env = Environment(
            loader=FileSystemLoader(str(directorio_archivos)),
            autoescape=select_autoescape(["html","xml"])
            )
            template = env.get_template("template.html")

            html_content = template.render(
                nombre=vol.nombre,
                apellidos=vol.apellidos,
                numerovoluntario=vol.numerovoluntario,
                año=vol.fechacreacion
            )

           
            yag = yagmail.SMTP(user=settings.EMAIL, password=settings.EMAIL_PASSWORD)
            # yagmail permite inline images con "cid:"
            
            yag.send(
                to=vol.email,
                subject="Bienvenido a RiverSpain 🌊",
                contents=[
                    html_content
                ],
                headers={"X-Mailer": "RiverSpainMailService/1.0"}
            )
            logging.info("Email enviado a %s", vol.email)
        except Exception as e:
            logging.error("Falló enviar_email_bienvenida para %s: %s", vol.email, e)
            # relanzamos como RuntimeError para uniformizar el catch en capas superiores
            raise RuntimeError(f"No se pudo enviar el email de bienvenida: {e}")















if __name__== "__main__":
    current_dir=os.path.dirname(os.path.abspath(__file__))
    recordatorio=os.path.join(current_dir,"salidas_pdf")
    recordatorio=os.path.join(recordatorio,
    "Recordatorio_Ana_Martínez.pdf")

    print(recordatorio)
    enviar_email_recordatorio(pdf_file_path=recordatorio,destinatario="ana@example.com")


