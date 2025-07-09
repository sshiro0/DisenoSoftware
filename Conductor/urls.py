from django.urls import path
from .views import *
urlpatterns = [
    path('Paquetes_entrega/', Ver_Paquetes_Entrega, name='ver_entregas'),
    path('Mapas/', Ver_ruta, name='ver_ruta'),
]