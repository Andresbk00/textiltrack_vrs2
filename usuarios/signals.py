from django.dispatch import receiver
from django.db.models.signals import post_save
from usuarios.utils.email_sendgrid import send_email_sendgrid
from django.conf import settings

from .models import Usuario
from .tokens import email_verification_token


@receiver(post_save, sender=Usuario)
def enviar_correo_verificacion(sender, instance, created, **kwargs):
    """
    Envía automáticamente un correo de verificación
    cuando el usuario es creado.
    """
    if created and not instance.email_verificado:  # <-- CORREGIDO

        token = email_verification_token.make_token(instance)
        uid = instance.pk

        from django.conf import settings
        link = f"{settings.SITE_URL}/verificar/{uid}/{token}/"

        asunto = "Confirma tu correo en TextilTrack"
        mensaje_html = (
            f"Hola {instance.first_name},<br><br>"
            "Por favor confirma tu dirección de correo usando el siguiente enlace:<br><br>"
            f"<a href='{link}'>{link}</a><br><br>"
            "Este enlace expirará en 2 horas.<br><br>"
            "Gracias,<br>El equipo de TextilTrack"
        )
        send_email_sendgrid(
            to_email=instance.email,
            subject=asunto,
            html_content=mensaje_html
        )

