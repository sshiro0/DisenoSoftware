from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_user),
    path('Paquetes/<int:id>/', views.Ver_Paquetes_Cliente, name='ver_paquetes_cliente'),
    path('Paquetes_entrega/', views.Ver_Paquetes_Entrega, name='ver_entregas'),
    path('Mapas/', views.Ver_ruta, name='ver_ruta'),
]