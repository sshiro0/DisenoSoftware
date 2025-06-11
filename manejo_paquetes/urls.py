from django.urls import path
from . import views

urlpatterns = [

    # Autenticación
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Admin
    path('admin/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    
    # Conductor
    path('conductor/', views.ConductorDashboardView.as_view(), name='conductor-dashboard'),
    path('conductor/ruta/', views.RutaOptimaView.as_view(), name='ruta-optima'),
    
    # Cliente
    path('cliente/', views.ClienteDashboardView.as_view(), name='cliente-dashboard'),
    path('cliente/paquetes/', views.PaquetesClienteView.as_view(), name='paquetes-cliente'),
]