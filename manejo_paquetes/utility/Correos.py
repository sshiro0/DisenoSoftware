from django.core.mail import send_mail

def enviar_correo(correo_destinatario, asunto, mensaje):
    send_mail(
        asunto,
        mensaje,
        'trabajoudec1@gmail.com', # De quién
        [correo_destinatario], # A quién
        fail_silently=False,
    )