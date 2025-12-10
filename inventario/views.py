from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from usuarios.models import Usuario
from .models import Producto, Categoria, MovimientoInventario, ProductoBaja
from .forms import CategoriaForm, ProductoForm, MovimientoForm
from .forms import ReporteProductoAgotadoForm
from .models import ReporteProductoAgotado



def solo_admin(user):
    return user.rol == "admin"

def solo_auxiliar(user):
    return user.rol == "auxiliar" or user.rol == "admin"

def solo_vendedor(user):
    return user.rol == "vendedor" or user.rol == "admin"


@login_required
def lista_productos(request):
    productos = Producto.objects.filter(estado="activo")
    return render(request, "inventario/lista_productos.html", {"productos": productos})



@login_required
def crear_producto(request):
    if request.user.rol not in ["administrador", "auxiliar"]:
        messages.error(request, "No tienes permisos para crear productos.")
        return redirect("inventario:lista_productos")

    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect("inventario:lista_productos")
    else:
        form = ProductoForm()

    return render(request, "inventario/crear_producto.html", {"form": form})



@login_required
def editar_producto(request, pk):
    if request.user.rol not in ["administrador", "auxiliar"]:
        messages.error(request, "No tienes permisos para editar productos.")
        return redirect("inventario:lista_productos")

    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado.")
            return redirect("inventario:lista_productos")
    else:
        form = ProductoForm(instance=producto)

    return render(request, "inventario/editar_producto.html", {"form": form})


@login_required
def eliminar_producto(request, pk):
    if request.user.rol not in ["administrador", "auxiliar"]:
        messages.error(request, "No tienes permisos para eliminar productos.")
        return redirect("inventario:lista_productos")

    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    messages.success(request, "Producto eliminado.")
    return redirect("inventario:lista_productos")


# Movimientos
@login_required
def movimientos(request):
    lista = MovimientoInventario.objects.all()
    return render(request, "inventario/movimientos.html", {"movimientos": lista})


@login_required
def registrar_movimiento(request):
    if request.user.rol not in ["auxiliar", "administrador"]:
        messages.error(request, "No tienes permisos para registrar movimientos.")
        return redirect("inventario:movimientos")

    if request.method == "POST":
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)

            # Actualizar stock
            if movimiento.tipo == "entrada":
                movimiento.producto.stock += movimiento.cantidad
            else:
                if movimiento.producto.stock < movimiento.cantidad:
                    messages.error(request, "Stock insuficiente.")
                    return redirect("inventario:registrar_movimiento")

                movimiento.producto.stock -= movimiento.cantidad

            movimiento.responsable = request.user.email
            movimiento.producto.save()
            movimiento.save()

            messages.success(request, "Movimiento registrado.")
            return redirect("inventario:movimientos")
    else:
        form = MovimientoForm()

    return render(request, "inventario/registrar_movimiento.html", {"form": form})


# ==========================================
# PANELES DEL VENDEDOR
# ==========================================

@login_required
def registrar_pedido(request):
    if request.user.rol not in ["vendedor", "administrador"]:
        messages.error(request, "No tienes permisos para registrar pedidos.")
        return redirect("panel_vendedor")

    if request.method == "POST":
        messages.success(request, "Pedido registrado correctamente.")
        return redirect("panel_vendedor")

    return render(request, "inventario/registrar_pedido.html")


@login_required
def generar_factura(request):
    if request.user.rol not in ["vendedor", "administrador"]:
        messages.error(request, "No tienes permisos para generar facturas.")
        return redirect("panel_vendedor")

    if request.method == "POST":
        messages.success(request, "Factura generada.")
        return redirect("panel_vendedor")

    return render(request, "inventario/generar_factura.html")


@login_required
def crear_cotizacion(request):
    if request.user.rol not in ["vendedor", "administrador"]:
        messages.error(request, "No tienes permisos para crear cotizaciones.")
        return redirect("panel_vendedor")

    if request.method == "POST":
        messages.success(request, "Cotización creada correctamente.")
        return redirect("panel_vendedor")

    return render(request, "inventario/crear_cotizacion.html")


def lista_productos_vendedor(request):
    productos = Producto.objects.filter(estado="activo")
    return render(request, "inventario/lista_productos_vendedor.html", {"productos": productos})



# inventario/views.py

@login_required
def dar_baja_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        motivo = request.POST.get("motivo")
        ProductoBaja.objects.create(
            producto=producto,
            motivo=motivo,
            responsable=request.user
        )

        producto.estado = "baja"
        producto.save()

        messages.success(request, "Producto dado de baja correctamente.")
        return redirect("inventario:lista_bajas")

    return render(request, "inventario/dar_baja.html", {"producto": producto})
@login_required
def lista_bajas(request):
    bajas = ProductoBaja.objects.all().order_by("-fecha")
    return render(request, "inventario/lista_bajas.html", {"bajas": bajas})


@login_required
def crear_reporte_agotado(request):
    if request.user.rol != "auxiliar":
        messages.error(request, "No tienes permiso para crear reportes.")
        return redirect('panel_aux')

    if request.method == "POST":
        form = ReporteProductoAgotadoForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.responsable = request.user
            reporte.save()
            messages.success(request, "Reporte enviado correctamente.")
            return redirect('panel_aux')
    else:
        form = ReporteProductoAgotadoForm()

    return render(request, "inventario/crear_reporte.html", {
        'form': form
    })


@login_required
def lista_reportes(request):
    if request.user.rol != "administrador":
        messages.error(request, "Solo el administrador puede ver los reportes.")
        return redirect('panel_admin')

    reportes = ReporteProductoAgotado.objects.all().order_by('-fecha')

    return render(request, "inventario/lista_reportes.html", {
        'reportes': reportes
    })


def lista_productos_vendedor(request):
    categoria_id = request.GET.get('categoria')

    productos = Producto.objects.all().select_related('categoria')
    categorias = Categoria.objects.all()

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    return render(request, 'inventario/lista_productos_vendedor.html', {
        'productos': productos,
        'categorias': categorias
    })

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    return render(request, 'inventario/detalle_producto.html', {
        'producto': producto
    })

def lista_productos(request):
    categoria = request.GET.get("categoria", "")

    productos = Producto.objects.all()

    # si filtra por categoría
    if categoria:
        productos = productos.filter(categoria__nombre=categoria)

    # obtener todas las categorías para el select
    categorias = Categoria.objects.all()

    context = {
        "productos": productos,
        "categorias": categorias,
        "categoria_seleccionada": categoria,
    }
    return render(request, "inventario/lista_productos.html", context)

