from django.db import models
from django.utils import timezone
from inventario.models import Producto

# ================================
# CLIENTES
# ================================
class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    documento = models.CharField(max_length=50, blank=True, null=True)

    def _str_(self):
        return self.nombre

# ================================
# COTIZACIONES
# ================================
class Cotizacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    detalle = models.TextField(blank=True)
    valor_estimado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    productos = models.ManyToManyField(Producto, through='DetalleCotizacion')

    def _str_(self):
        return f"Cotización #{self.id} - {self.cliente.nombre}"

class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey('Cotizacion', on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad

# ================================
# FACTURAS
# ================================
class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(blank=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    productos = models.ManyToManyField(Producto, through='DetalleFactura')

    def _str_(self):
        return f"Factura #{self.id} - {self.cliente.nombre}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey('Factura', on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad

# ================================
# PEDIDOS
# ================================
class Pedido(models.Model):
    ESTADOS = (
        ("pendiente", "Pendiente"),
        ("proceso", "En proceso"),
        ("completado", "Completado"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    notas = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    productos = models.ManyToManyField(Producto, through='DetallePedido')

    def _str_(self):
        return f"Pedido #{self.id} - {self.cliente.nombre}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad


