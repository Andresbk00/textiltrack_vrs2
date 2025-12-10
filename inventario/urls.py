from django.urls import path
from . import views

app_name = "inventario"

urlpatterns = [
    path("productos/", views.lista_productos, name="lista_productos"),
    path("productos/nuevo/", views.crear_producto, name="crear_producto"),
    path("productos/editar/<int:pk>/", views.editar_producto, name="editar_producto"),
    path("productos/eliminar/<int:pk>/", views.eliminar_producto, name="eliminar_producto"),

    path("movimientos/", views.movimientos, name="movimientos"),
    path("movimientos/nuevo/", views.registrar_movimiento, name="registrar_movimiento"),

    path("productos/vendedor/", views.lista_productos_vendedor, name="lista_productos_vendedor"),


    path("pedidos/nuevo/", views.registrar_pedido, name="registrar_pedido"),
    path("factura/nueva/", views.generar_factura, name="generar_factura"),
    path("cotizacion/nueva/", views.crear_cotizacion, name="crear_cotizacion"),

    path("producto/<int:pk>/baja/", views.dar_baja_producto, name="dar_baja_producto"),
    path("bajas/", views.lista_bajas, name="lista_bajas"),
    path('reporte/crear/', views.crear_reporte_agotado, name='crear_reporte_agotado'),
    path('reportes/', views.lista_reportes, name='lista_reportes'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),

]



