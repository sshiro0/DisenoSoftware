from django.urls import path
from . import views

urlpatterns = [
    path('Paquetes/<int:id>/', views.Ver_Paquetes_Cliente, name='ver_paquetes_cliente'),
]