from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from usuarios.utils.email_sendgrid import send_email_sendgrid
from django.views.decorators.http import require_POST
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
import re

from .forms import RegistroUsuarioForm
from .tokens import email_verification_token

Usuario = get_user_model()

# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------
def home_view(request):
    return render(request, 'usuarios/home.html')

# ---------------------------------------------------------
# REGISTRO
# ---------------------------------------------------------
def web_register(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()

            # VERIFICACIÓN DE CORREO
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = email_verification_token.make_token(user)
            link = f"{settings.SITE_URL}/verificar/{uid}/{token}/"


            send_email_sendgrid(
                to_email=user.email,
                subject="Verificación de correo - TextilTrack",
                html_content=f"Hola {user.first_name}, verifica tu correo aquí: <a href='{link}'>{link}</a>"
            )

            messages.success(request, "Te enviamos un correo para verificar tu cuenta.")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)

    form = RegistroUsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})

# ---------------------------------------------------------
# VERIFICACIÓN EMAIL
# ---------------------------------------------------------
def verificar_email(request, uid, token):
    try:
        uid_decoded = force_str(urlsafe_base64_decode(uid))
        user = Usuario.objects.get(pk=uid_decoded)
    except:
        messages.error(request, "Enlace inválido.")
        return redirect('login')

    if email_verification_token.check_token(user, token):
        user.email_verificado = True
        user.save()
        messages.success(request, "Correo verificado. Espera aprobación.")
        return redirect('login')

    messages.error(request, "Token inválido.")
    return redirect('login')

# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------
def web_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, 'Credenciales incorrectas.')
            return redirect('login')

        # 🔹 CORREO NO VERIFICADO
        if not user.email_verificado:
            messages.warning(request, 'Por favor confirma tu correo para activar tu cuenta.')
            return redirect('login')

        # 🔹 CUENTA PENDIENTE
        if user.estado == 'pendiente':
            messages.info(request, 'Tu cuenta está en proceso de activación. Un administrador revisará tu solicitud.')
            return redirect('login')

        # 🔹 CUENTA DESACTIVADA / BLOQUEADA
        if user.estado == 'inactivo':
            messages.error(request, 'Cuenta temporalmente bloqueada. Comuníquese con el administrador.')
            return redirect('login')

        # 🔹 Ahora sí validamos la contraseña
        auth_user = authenticate(request, username=user.username, password=password)

        if auth_user:
            login(request, auth_user)

            # Redirigir según rol
            if user.rol == 'administrador':
                return redirect('panel_admin')
            elif user.rol == 'vendedor':
                return redirect('panel_vendedor')
            else:
                return redirect('panel_aux')

        # 🔹 Contraseña incorrecta
        messages.error(request, "Credenciales incorrectas.")
        return redirect('login')

    return render(request, 'usuarios/login.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FotoPerfilForm

@login_required
def perfil(request):
    usuario = request.user
    
    if request.method == 'POST':
        form = FotoPerfilForm(request.POST, request.FILES, instance=usuario)
        
        if form.is_valid():
            try:
                # Verificar que hay un archivo
                if 'foto_perfil' in request.FILES:
                    form.save()
                    messages.success(request, '✅ Foto de perfil actualizada correctamente')
                else:
                    messages.warning(request, '⚠️ No se seleccionó ninguna imagen')
                    
                return redirect('perfil')
                
            except Exception as e:
                messages.error(request, f'❌ Error al guardar la foto: {str(e)}')
                print(f"Error al guardar foto: {e}")  # Para debug en consola
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
    else:
        form = FotoPerfilForm(instance=usuario)

    return render(request, 'usuarios/perfil.html', {'form': form})


# ---------------------------------------------------------
# RESET PASSWORD — SOLICITUD
# ---------------------------------------------------------
def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, "No existe una cuenta con ese correo.")
            return redirect('password_reset_request')

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"{settings.SITE_URL}/reset_password/{uid}/{token}/"

        send_email_sendgrid(
            to_email=email,
            subject="Restablecer contraseña — TextilTrack",
            html_content=f"Ingresa aquí para restablecer tu contraseña: <a href='{reset_link}'>{reset_link}</a>"
        )

        messages.success(request, "Se envió un enlace a tu correo.")
        return redirect('login')

    return render(request, 'usuarios/password_reset_request.html')

# ---------------------------------------------------------
# RESET PASSWORD — CONFIRMAR NUEVA
# ---------------------------------------------------------
def reset_password_confirm(request, uid, token):
    try:
        uid_decoded = force_str(urlsafe_base64_decode(uid))
        user = Usuario.objects.get(pk=uid_decoded)
    except Exception as e:
        from usuarios.models import EmailLog
        EmailLog.objects.create(
            destinatario='Desconocido',
            asunto='Intento de restablecimiento de contraseña',
            contenido=f"Token inválido: {uid} | {token}",
            exito=False,
            error=str(e)
        )
        messages.error(request, "Enlace inválido.")
        return redirect('login')

    if not default_token_generator.check_token(user, token):
        from usuarios.models import EmailLog
        EmailLog.objects.create(
            destinatario=user.email,
            asunto='Token de restablecimiento inválido',
            contenido=f"Token: {token}",
            exito=False,
            error='Token inválido o expirado'
        )
        messages.error(request, "Este enlace ha expirado.")
        return redirect('login')

    if request.method == 'POST':
        new_password = request.POST.get('password')
        # Validación fuerte de contraseña (igual que en forms.py)
        errores = []
        if len(new_password) < 8:
            errores.append("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r"[A-Z]", new_password):
            errores.append("La contraseña debe incluir una mayúscula.")
        if not re.search(r"[0-9]", new_password):
            errores.append("La contraseña debe incluir un número.")
        if not re.search(r"[\W_]", new_password):
            errores.append("La contraseña debe incluir un carácter especial.")
        if errores:
            for err in errores:
                messages.error(request, err)
            return render(request, 'usuarios/reset_password_confirm.html')
        user.set_password(new_password)
        user.save()
        messages.success(request, "Tu contraseña ha sido actualizada.")
        return redirect('login')

    return render(request, 'usuarios/reset_password_confirm.html')

# ---------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect('login')

# ---------------------------------------------------------
# PANEL ADMIN
# ---------------------------------------------------------
@login_required
def panel_admin(request):
    usuarios = Usuario.objects.all()
    saludo = f"¡Hola {request.user.first_name}! Bienvenido, Administrador."
    return render(request, 'usuarios/panel_admin.html', {
        'usuarios': usuarios,
        'saludo': saludo
    })

@require_POST
@login_required
def aprobar_usuario(request, user_id):
    user = Usuario.objects.get(id=user_id)
    user.aprobar()
    messages.success(request, "Usuario aprobado.")
    return redirect('panel_admin')

@require_POST
@login_required
def desactivar_usuario(request, user_id):
    user = Usuario.objects.get(id=user_id)
    user.desactivar()
    messages.warning(request, "Usuario desactivado.")
    return redirect('panel_admin')

@require_POST
@login_required
def reactivar_usuario(request, user_id):
    user = Usuario.objects.get(id=user_id)
    user.reactivar()
    messages.success(request, "Usuario reactivado.")
    return redirect('panel_admin')

@require_POST
@login_required
def eliminar_usuario(request, user_id):
    user = Usuario.objects.get(id=user_id)
    user.delete()
    messages.success(request, "Usuario eliminado.")
    return redirect('panel_admin')

# ---------------------------------------------------------
# PANEL VENDEDOR / AUX
# ---------------------------------------------------------
from django.shortcuts import render
from ventas.models import Cliente, Cotizacion, Factura, Pedido


def panel_vendedor(request):
    total_clientes = Cliente.objects.count()
    total_cotizaciones = Cotizacion.objects.count()
    total_facturas = Factura.objects.count()
    total_pedidos = Pedido.objects.count()

    saludo = f"¡Hola {request.user.first_name}! Bienvenido, Vendedor."


    pedidos_pendientes = Pedido.objects.filter(estado="pendiente").count()
    pedidos_proceso = Pedido.objects.filter(estado="proceso").count()
    pedidos_completados = Pedido.objects.filter(estado="completado").count()

    return render(request, "usuarios/panel_vendedor.html", {
        "total_clientes": total_clientes,
        "total_cotizaciones": total_cotizaciones,
        "total_facturas": total_facturas,
        "total_pedidos": total_pedidos,

        "pendientes": pedidos_pendientes,
        "proceso": pedidos_proceso,
        "completados": pedidos_completados,
        "saludo": saludo,
    })

from django.contrib.auth.decorators import login_required

@login_required
def panel(request):
    usuario = request.user
    return render(request, "usuarios/panel.html", {"user": usuario})


@login_required
def panel_aux(request):
    saludo = f"¡Hola {request.user.first_name}! Bienvenido, Auxiliar de Inventario."
    return render(request, 'usuarios/panel_aux.html', {
        'saludo': saludo
    })
