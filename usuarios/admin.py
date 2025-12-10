from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'rol', 'aprobado', 'is_active', 'estado', 'fecha_creacion')
    list_filter = ('rol', 'aprobado', 'is_active', 'estado')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('fecha_creacion',)

