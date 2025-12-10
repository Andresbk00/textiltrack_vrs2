from django.core.management.base import BaseCommand
from inventario.models import Categoria, Producto

class Command(BaseCommand):
    help = 'Crea 20 productos iniciales con sus categorías asignadas'

    def handle(self, *args, **kwargs):
        productos = [
            ("Tela Algodón 180g – Blanca", "Tela en rollos", 18000, 50),
            ("Tela Polyester Lycra – Negra", "Tela en rollos", 22000, 40),
            ("Tela Denim 12 onzas", "Tela en rollos", 35000, 30),
            ("Tela Antifluido Médico – Azul", "Telas especializadas", 28000, 40),
            ("Tela Acolchada Doble Capa", "Telas especializadas", 45000, 20),

            ("Camiseta Básica Unisex – Blanca", "Confecciones terminadas", 15000, 100),
            ("Pantalón Jogger – Negro", "Confecciones terminadas", 38000, 60),
            ("Chaqueta Rompevientos", "Confecciones terminadas", 60000, 25),
            ("Buzo Hoodie – Algodón", "Confecciones terminadas", 52000, 30),
            ("Short Deportivo – Lycra", "Confecciones terminadas", 25000, 50),

            ("Hilo Poliester 3000Y – Blanco", "Hilos y fibras", 8000, 120),
            ("Hilo Nylon para Costura Resistente", "Hilos y fibras", 9000, 100),
            ("Elástico Plano 3cm – Negro", "Elasticados", 12000, 80),
            ("Elástico Redondo para Tapabocas", "Elasticados", 5000, 150),

            ("Cremalleras Metálicas #5 – Negro", "Accesorios de costura", 1500, 200),
            ("Botones 20mm", "Accesorios de costura", 700, 300),
            ("Broches Plásticas para Mochila", "Accesorios de costura", 2500, 150),

            ("Etiquetas Tejidas Marca Genérica", "Trims / Etiquetas", 500, 500),
            ("Marquillas Estampadas Talla S-M-L", "Trims / Etiquetas", 300, 400),

            ("Vinilo Textil Termoadhesivo – Negro", "Insumos de estampado / serigrafía", 9000, 60),
        ]

        for nombre, categoria_nombre, precio, stock in productos:
            categoria, _ = Categoria.objects.get_or_create(nombre=categoria_nombre)
            Producto.objects.get_or_create(
                nombre=nombre,
                categoria=categoria,
                precio=precio,
                stock=stock
            )

        self.stdout.write(self.style.SUCCESS("Productos creados correctamente"))
