from django.contrib import admin

# Register your models here.
# inventario/admin.py

from django.contrib import admin
from .models import Categoria

admin.site.register(Categoria)
