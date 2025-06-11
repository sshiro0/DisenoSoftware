from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    #redirección postlogin
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    path('dashboard/cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('dashboard/conductor/', views.dashboard_conductor, name='dashboard_conductor'),

    path('Paquetes/<int:id>', views.Ver_Paquetes_Cliente),
    path('Paquetes_entrega/', views.Ver_Paquetes_Entrega),
    path('Mapas/', views.Ver_ruta),
]