from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.pagina_inicio, name='inicio'),
    path('Paquetes/<int:id>', views.Ver_Paquetes_Cliente),
    path('camionero/', views.pagina_camionero, name='camionero'),
    path('cliente/', views.pagina_cliente, name='cliente'),
    path('Paquetes/<int:id>/', views.Ver_Paquetes_Cliente, name='ver_paquetes'),
]