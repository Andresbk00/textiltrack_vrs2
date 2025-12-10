from django.db import models
from django.utils import timezone

ESTADOS_PRODUCTO = [
    ('activo', 'Activo'),
    ('baja', 'Dado de Baja'),
]

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre



class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    stock_minimo = models.IntegerField(default=5)
    estado = models.CharField(max_length=20, choices=ESTADOS_PRODUCTO, default='activo')

    def esta_bajo(self):
        return self.stock <= self.stock_minimo and self.stock > 0

    def esta_agotado(self):
        return self.stock == 0

    def __str__(self):
        return self.nombre

    def _str_(self):
        return self.nombre


class MovimientoInventario(models.Model):
    TIPO = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida')
    )

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(default=timezone.now)
    responsable = models.CharField(max_length=100)

    def _str_(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"



# inventario/models.py

class ProductoBaja(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    motivo = models.TextField()
    responsable = models.ForeignKey("usuarios.Usuario", on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Baja - {self.producto.nombre}"


# ============================
#   REPORTES DE PRODUCTO AGOTADO
# ============================

class ReporteProductoAgotado(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=255, default="Producto agotado")
    destinatario = models.CharField(max_length=100, default="Administrador")
    responsable = models.ForeignKey("usuarios.Usuario", on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte - {self.producto.nombre} ({self.fecha.strftime('%d/%m/%Y')})"
