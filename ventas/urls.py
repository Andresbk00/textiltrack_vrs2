from django.urls import path
from . import views

app_name = "ventas"

urlpatterns = [
    # CLIENTES
    path("clientes/", views.lista_clientes, name="lista_clientes"),
    path("clientes/nuevo/", views.crear_cliente, name="crear_cliente"),
    path("clientes/editar/<int:pk>/", views.editar_cliente, name="editar_cliente"),
    path("clientes/eliminar/<int:pk>/", views.eliminar_cliente, name="eliminar_cliente"),

    # COTIZACIONES
    path("cotizaciones/nueva/", views.crear_cotizacion, name="crear_cotizacion"),
    path("cotizaciones/<int:pk>/", views.detalle_cotizacion, name="detalle_cotizacion"),
    path("cotizaciones/<int:pk>/descargar/", views.descargar_cotizacion_pdf, name="descargar_cotizacion"),
    path("cotizaciones/", views.lista_cotizaciones, name="lista_cotizaciones"),

    # FACTURAS
    path("facturas/nueva/", views.crear_factura, name="crear_factura"),
    path("facturas/<int:pk>/", views.detalle_factura, name="detalle_factura"),
    path("facturas/<int:pk>/descargar/", views.descargar_factura_pdf, name="descargar_factura"),
    path("facturas/", views.lista_facturas, name="lista_facturas"),

    # PEDIDOS
    path("pedidos/nuevo/", views.crear_pedido, name="crear_pedido"),
    path("pedidos/", views.lista_pedidos, name="lista_pedidos"),
    path("pedidos/<int:pk>/", views.detalle_pedido, name="detalle_pedido"),
    path("pedidos/<int:pk>/estado/", views.actualizar_estado_pedido, name="actualizar_estado_pedido"),

]


