import yagmail
import os
import dotenv
dotenv.load_dotenv()

EMAIL=os.getenv("EMAIL","correo@gmail.com")
PASSWORD=os.getenv("EMAIL_PASSWORD","password")

def enviar_email(pdf_file_path, destinatario):
    print(EMAIL)
    print(PASSWORD)
    # Autenticación de Gmail
    yag = yagmail.SMTP(user=EMAIL, password=PASSWORD)

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
    "Recordatorio_ANA_Martínez.pdf")

    print(recordatorio)
    enviar_email(pdf_file_path=recordatorio,destinatario="example@gmail.com")
