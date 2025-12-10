from django.contrib import admin
from .models import Cliente, Cotizacion, Factura, Pedido, DetallePedido

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "email", "telefono")
    search_fields = ("nombre", "documento", "email")

@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "fecha", "valor_estimado")
    search_fields = ("cliente__nombre",)
    list_filter = ("fecha",)

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "fecha", "monto")
    search_fields = ("cliente__nombre",)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "fecha", "estado")
    search_fields = ("cliente__nombre",)
    list_filter = ("estado", "fecha")

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "pedido", "producto", "cantidad")

