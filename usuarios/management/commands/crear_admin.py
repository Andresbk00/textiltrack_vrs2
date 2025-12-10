from django.core.management.base import BaseCommand
from usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Crea el usuario admin inicial'

    def handle(self, *args, **kwargs):
        email = 'gcamiloandres60@gmail.com'
        username = 'gcamiloandres60'
        existe_email = Usuario.objects.filter(email=email).exists()
        existe_username = Usuario.objects.filter(username=username).exists()
        if not existe_email and not existe_username:
            Usuario.objects.create_user(
                username=username,
                email=email,
                password='adminTemp2025',
                rol='administrador',
                aprobado=True,
                estado='activo',
                email_verificado=True,
                is_staff=True,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS('Usuario admin creado'))
        else:
            self.stdout.write(self.style.WARNING('El usuario admin ya existe (por email o username)'))
