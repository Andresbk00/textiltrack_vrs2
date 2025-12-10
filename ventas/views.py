from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.db import transaction

from inventario.models import Producto
from .models import Cliente, Pedido, DetallePedido, Factura, DetalleFactura, Cotizacion, DetalleCotizacion
from xhtml2pdf import pisa


# ---------------------------
# FUNCIÓN PARA GENERAR PDF
# ---------------------------
def render_pdf(template_src, context={}):
    template = get_template(template_src)
    html = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=documento.pdf"
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generando el PDF")
    return response


# ---------------------------
# CLIENTES
# ---------------------------
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "ventas/clientes/lista.html", {"clientes": clientes})


def crear_cliente(request):
    if request.method == "POST":
        Cliente.objects.create(
            nombre=request.POST.get("nombre"),
            email=request.POST.get("email"),
            telefono=request.POST.get("telefono"),
            direccion=request.POST.get("direccion"),
            documento=request.POST.get("documento")
        )
        messages.success(request, "Cliente creado correctamente.")
        return redirect("ventas:lista_clientes")

    return render(request, "ventas/clientes/crear.html")


def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        
        cliente.email = request.POST.get("email")
        cliente.telefono = request.POST.get("telefono")
        cliente.direccion = request.POST.get("direccion")
        
        cliente.save()

        messages.success(request, "Cliente actualizado correctamente.")
        return redirect("ventas:lista_clientes")

    return render(request, "ventas/clientes/editar.html", {"cliente": cliente})


def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        cliente.delete()
        messages.success(request, "Cliente eliminado.")
        return redirect("ventas:lista_clientes")

    return render(request, "ventas/clientes/eliminar.html", {"cliente": cliente})


# ---------------------------
# PEDIDOS
# ---------------------------
@transaction.atomic
def crear_pedido(request):
    clientes = Cliente.objects.all()
    productos = Producto.objects.filter(estado="activo")   # SOLO ACTIVOS

    if request.method == "POST":
        cliente_id = request.POST.get("cliente")
        producto_ids = request.POST.getlist("producto_ids")
        notas = request.POST.get("notas", "")

        if not cliente_id:
            messages.error(request, "Selecciona un cliente.")
            return redirect("ventas:crear_pedido")

        if not producto_ids:
            messages.error(request, "Debes seleccionar al menos un producto.")
            return redirect("ventas:crear_pedido")

        cliente = get_object_or_404(Cliente, pk=cliente_id)
        pedido = Pedido.objects.create(cliente=cliente, notas=notas, estado="proceso")
        total_monto = 0

        for pid in producto_ids:
            cantidad_str = request.POST.get(f"cantidad_{pid}", "0")

            try:
                cantidad = int(cantidad_str)
            except ValueError:
                cantidad = 0

            if cantidad <= 0:
                continue

            producto = get_object_or_404(Producto, pk=pid, estado="activo")

            # 🚫 Producto agotado → NO se puede usar
            if producto.stock <= 0:
                messages.error(request, f"El producto '{producto.nombre}' está agotado y no puede usarse.")
                pedido.delete()
                return redirect("ventas:crear_pedido")

            # 🚫 Stock insuficiente
            if producto.stock < cantidad:
                messages.error(request, f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")
                pedido.delete()
                return redirect("ventas:crear_pedido")

            # Actualizar stock y registrar detalle
            producto.stock -= cantidad
            producto.save()

            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad
            )

            total_monto += producto.precio * cantidad

        # Crear factura automática
        factura = Factura.objects.create(
            cliente=cliente,
            descripcion=f"Factura generada automáticamente por Pedido #{pedido.id}",
            monto=total_monto
        )

        for d in pedido.detalles.all():
            DetalleFactura.objects.create(
                factura=factura,
                producto=d.producto,
                cantidad=d.cantidad
            )

        messages.success(request, f"Pedido #{pedido.id} creado correctamente y factura #{factura.id} generada.")
        return redirect("ventas:detalle_pedido", pedido.pk)

    return render(request, "ventas/pedidos/crear.html", {
        "clientes": clientes,
        "productos": productos
    })


def detalle_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    # Si es vendedor → plantilla especial SIN opciones de actualización
    if request.user.rol == "vendedor":
        return render(request, "ventas/pedidos/detalle_vendedor.html", {
            "pedido": pedido
        })

    # Para admin o auxiliar → plantilla normal
    return render(request, "ventas/pedidos/detalle.html", {
        "pedido": pedido
    })



def actualizar_estado_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == "POST":
        pedido.estado = request.POST.get("estado")
        pedido.save()
        messages.success(request, "Estado actualizado.")
        return redirect("ventas:detalle_pedido", pedido.pk)

    return render(request, "ventas/pedidos/estado.html", {"pedido": pedido})


# ---------------------------
# COTIZACIONES
# ---------------------------
def crear_cotizacion(request):
    clientes = Cliente.objects.all()
    productos = Producto.objects.filter(estado="activo")  # SOLO ACTIVOS

    if request.method == "POST":
        cliente_id = request.POST.get("cliente")

        if not cliente_id:
            messages.error(request, "Selecciona un cliente.")
            return redirect("ventas:crear_cotizacion")

        cliente = get_object_or_404(Cliente, pk=cliente_id)

        detalle = ""
        total_valor = 0

        productos_list = request.POST.getlist("producto")
        cantidades_list = request.POST.getlist("cantidad")

        for pid, cant in zip(productos_list, cantidades_list):
            if not pid or not cant:
                continue

            try:
                cantidad = int(cant)
            except ValueError:
                continue

            producto = get_object_or_404(Producto, pk=pid, estado="activo")

            # 🚫 Bloqueo: agotado = NO cotizable
            if producto.stock <= 0:
                messages.error(request, f"El producto '{producto.nombre}' está agotado y no puede cotizarse.")
                return redirect("ventas:crear_cotizacion")

            detalle += f"{producto.nombre} x {cantidad} = ${producto.precio * cantidad}\n"
            total_valor += producto.precio * cantidad

        cot = Cotizacion.objects.create(
            cliente=cliente,
            detalle=detalle,
            valor_estimado=total_valor
        )

        # Guardar detalles
        for pid, cant in zip(productos_list, cantidades_list):
            if not pid or not cant:
                continue

            try:
                cantidad = int(cant)
            except ValueError:
                continue

            producto = get_object_or_404(Producto, pk=pid, estado="activo")

            DetalleCotizacion.objects.create(
                cotizacion=cot,
                producto=producto,
                cantidad=cantidad
            )

        messages.success(request, "Cotización creada correctamente.")
        return redirect("ventas:detalle_cotizacion", cot.pk)

    return render(request, "ventas/cotizaciones/crear.html", {
        "clientes": clientes,
        "productos": productos
    })


def detalle_cotizacion(request, pk):
    cot = get_object_or_404(Cotizacion, pk=pk)
    return render(request, "ventas/cotizaciones/detalle.html", {"cot": cot})


def descargar_cotizacion_pdf(request, pk):
    cot = get_object_or_404(Cotizacion, pk=pk)
    return render_pdf("ventas/cotizaciones/pdf.html", {"cot": cot})


# ---------------------------
# FACTURAS
# ---------------------------
def crear_factura(request):
    clientes = Cliente.objects.all()
    productos = Producto.objects.filter(estado="activo")

    if request.method == "POST":
        cliente_id = request.POST.get("cliente")

        if not cliente_id:
            messages.error(request, "Selecciona un cliente.")
            return redirect("ventas:crear_factura")

        cliente = get_object_or_404(Cliente, pk=cliente_id)

        detalle = ""
        total_valor = 0

        productos_list = request.POST.getlist("producto")
        cantidades_list = request.POST.getlist("cantidad")

        for pid, cant in zip(productos_list, cantidades_list):
            if not pid or not cant:
                continue

            try:
                cantidad = int(cant)
            except ValueError:
                continue

            producto = get_object_or_404(Producto, pk=pid, estado="activo")

            # 🚫 NO facturar agotado
            if producto.stock <= 0:
                messages.error(request, f"El producto '{producto.nombre}' está agotado y no puede facturarse.")
                return redirect("ventas:crear_factura")

            detalle += f"{producto.nombre} x {cantidad} = ${producto.precio * cantidad}\n"
            total_valor += producto.precio * cantidad

        factura = Factura.objects.create(
            cliente=cliente,
            descripcion=detalle,
            monto=total_valor
        )

        # Guardar detalles
        for pid, cant in zip(productos_list, cantidades_list):
            if not pid or not cant:
                continue

            try:
                cantidad = int(cant)
            except ValueError:
                continue

            producto = get_object_or_404(Producto, pk=pid, estado="activo")

            DetalleFactura.objects.create(
                factura=factura,
                producto=producto,
                cantidad=cantidad
            )

        messages.success(request, "Factura creada correctamente.")
        return redirect("ventas:detalle_factura", factura.pk)

    return render(request, "ventas/facturas/crear.html", {
        "clientes": clientes,
        "productos": productos
    })


def detalle_factura(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    return render(request, "ventas/facturas/detalle.html", {"factura": factura})


def descargar_factura_pdf(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    return render_pdf("ventas/facturas/pdf.html", {"factura": factura})


# -----------------------------
# LISTAS
# -----------------------------
def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, "ventas/pedidos/lista.html", {"pedidos": pedidos})


def lista_facturas(request):
    facturas = Factura.objects.all()
    return render(request, "ventas/facturas/lista.html", {"facturas": facturas})


def lista_cotizaciones(request):
    cotizaciones = Cotizacion.objects.all()
    return render(request, "ventas/cotizaciones/lista.html", {"cotizaciones": cotizaciones})
