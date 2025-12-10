from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
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

        link = f"http://127.0.0.1:8000/verificar/{uid}/{token}/"  # Ajusta a tu URL de verificación actual

        asunto = "Confirma tu correo en TextilTrack"
        mensaje = (
            f"Hola {instance.first_name},\n\n"
            "Por favor confirma tu dirección de correo usando el siguiente enlace:\n\n"
            f"{link}\n\n"
            "Este enlace expirará en 2 horas.\n\n"
            "Gracias,\nEl equipo de TextilTrack"
        )

        send_mail(
            asunto,
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )

