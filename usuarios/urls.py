from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),

    path('registro/', views.web_register, name='registro'),
    path('login/', views.web_login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Verificación email
    path('verificar/<uid>/<token>/', views.verificar_email, name='verificar_email'),

    # RESET PASSWORD (flujo correcto)
    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('reset_password/<uid>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),

    # Paneles
    path('panel_admin/', views.panel_admin, name='panel_admin'),
    path('panel_vendedor/', views.panel_vendedor, name='panel_vendedor'),
    path('panel_aux/', views.panel_aux, name='panel_aux'),

    # Acciones admin
    path('aprobar/<int:user_id>/', views.aprobar_usuario, name='aprobar_usuario'),
    path('desactivar/<int:user_id>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('reactivar/<int:user_id>/', views.reactivar_usuario, name='reactivar_usuario'),
    path('eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    path('perfil/', views.perfil, name='perfil'),
    
] 
