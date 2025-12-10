from django.core.management.base import BaseCommand
from usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Crea el usuario admin inicial'

    def handle(self, *args, **kwargs):
        if not Usuario.objects.filter(username='gcamiloandres60').exists():
            Usuario.objects.create_user(
                username='gcamiloandres60',
                email='gcamiloandres60@gmail.com',
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
            self.stdout.write(self.style.WARNING('El usuario admin ya existe'))
