from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),       # tus urls de usuarios
    path('ventas/', include('ventas.urls')),  # tus urls de ventas
    path('inventario/', include('inventario.urls')),  # urls inventario
]

# Esto es lo importante para que Django sirva los archivos media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
