from django.urls import path
from . import views
urlpatterns = [
    path('', views.hello),
    path('Paquetes/<int:id>', views.Ver_Paquetes_Cliente),
    path('Paquetes_entrega/', views.Ver_Paquetes_Entrega),
    path('Mapas/', views.Ver_ruta),
]