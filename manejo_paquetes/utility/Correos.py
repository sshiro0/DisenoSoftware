from django.core.mail import send_mail
from django.conf import settings

def enviar_correo(correo_destinatario, asunto, mensaje):
    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL, # De quién
        [correo_destinatario], # A quién
        fail_silently=False,
    )