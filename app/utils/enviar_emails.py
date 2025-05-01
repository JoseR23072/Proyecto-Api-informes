import yagmail
import os
from config.settings import settings
import logging

def enviar_email_recordatorio(pdf_file_path, destinatario):
    logging.info(f"El email es : {settings.EMAIL}")
    logging.info(f"La contraseña del envio del correo es : {settings.EMAIL_PASSWORD}")
    # Autenticación de Gmail
    yag = yagmail.SMTP(user=settings.EMAIL, password=settings.EMAIL_PASSWORD)

    asunto="Recordatorio Batida RiverSpain: ¡Nos encontramos en la acción!"
    cuerpo_email = """\
Estimado/a voluntario/a,

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

    print("Correo enviado con éxito!")

if __name__== "__main__":
    current_dir=os.path.dirname(os.path.abspath(__file__))
    recordatorio=os.path.join(current_dir,"salidas_pdf")
    recordatorio=os.path.join(recordatorio,
    "Recordatorio_Ana_Martínez.pdf")

    print(recordatorio)
    enviar_email_recordatorio(pdf_file_path=recordatorio,destinatario="ana@example.com")
