from django.core.management.base import BaseCommand
from inventario.models import Categoria

class Command(BaseCommand):
    help = 'Crea las categorías iniciales del sistema'

    def handle(self, *args, **kwargs):
        categorias = [
            "Tela en rollos",
            "Confecciones terminadas",
            "Hilos y fibras",
            "Accesorios de costura",
            "Tallas / Etiquetas",
            "Elasticados",
            "Cintas y sesgos",
            "Telas especializadas",
            "Insumos de estampado / serigrafía",
            "Embalajes y empaques"
        ]

        for nombre in categorias:
            Categoria.objects.get_or_create(nombre=nombre)

        self.stdout.write(self.style.SUCCESS("Categorías creadas correctamente"))
