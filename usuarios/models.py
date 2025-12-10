from django.db import models
# Log de correos enviados
class EmailLog(models.Model):
    destinatario = models.EmailField()
    asunto = models.CharField(max_length=255)
    contenido = models.TextField()
    exito = models.BooleanField(default=False)
    error = models.TextField(blank=True, null=True)
    fch_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.destinatario} | {self.asunto} | {self.fch_envio:%Y-%m-%d %H:%M}" 
# usuarios/models.py
from django.contrib.auth.models import AbstractUser

ROLES = [
    ('administrador', 'Administrador'),
    ('vendedor', 'Vendedor'),
    ('auxiliar', 'Auxiliar de Inventario'),
]

ESTADOS = [
    ('activo', 'Activo'),
    ('inactivo', 'Inactivo'),
    ('pendiente', 'Pendiente'),
]

class Usuario(AbstractUser):
    rol = models.CharField(max_length=20, choices=ROLES, default='vendedor')
    aprobado = models.BooleanField(default=False)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='pendiente')
    email_verificado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)  # <- Nueva

    def aprobar(self):
        self.aprobado = True
        self.is_active = True
        self.estado = 'activo'
        self.save()

    def desactivar(self):
        self.is_active = False
        self.estado = 'inactivo'
        self.save()

    def reactivar(self):
        self.is_active = True
        self.estado = 'activo'
        self.save()

    def __str__(self):
        return f"{self.username} ({self.rol})"


# inventario/models.py

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def _str_(self):
        return self.nombre
