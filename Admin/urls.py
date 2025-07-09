from django.urls import path
from . import views

urlpatterns = [
    path('Admin_Paquete/', views.create_paquete, name='admin_paquete'),
    path('Admin/', views.Admin, name='admin_login'),
    path('Admin_CrearConductor/', views.crear_usuario_general, name='admin_create_conductor')
]


