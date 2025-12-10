import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from usuarios.models import EmailLog

def send_email_sendgrid(to_email, subject, html_content):
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    exito = False
    error = ''
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        exito = response.status_code == 202
        return response.status_code
    except Exception as e:
        error = str(e)
        return error
    finally:
        EmailLog.objects.create(
            destinatario=to_email,
            asunto=subject,
            contenido=html_content,
            exito=exito,
            error=error
        )
