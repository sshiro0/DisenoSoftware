from django.urls import path
from . import views
urlpatterns = [
    path('', views.hello),
    path('Paquetes/<int:id>', views.Ver_Paquetes_Cliente)
]