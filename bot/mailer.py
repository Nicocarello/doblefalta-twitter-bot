import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bot.config import EMAIL_CONFIG

def enviar_reporte_email(cuerpo_email):
    """ Envía un correo con el resumen de la actividad del bot. """
    sender = EMAIL_CONFIG['sender']
    password = EMAIL_CONFIG['password']
    receivers = EMAIL_CONFIG['receivers']

    if not sender or not password or not receivers:
        print("⚠️ Configuración de email incompleta. No se enviará correo.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(receivers)
    msg['Subject'] = f"Reporte Bot Doble Falta - Tenistas Argentinos"

    # Adjuntar el cuerpo del mensaje
    msg.attach(MIMEText(cuerpo_email, 'plain'))

    try:
        # Configuración para Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())
        server.quit()
        print(f"📧 Reporte enviado con éxito a: {', '.join(receivers)}")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
