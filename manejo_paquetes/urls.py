from django.urls import path
from . import views
urlpatterns = [
    path('', views.hello),
    path('Paquetes/<int:id>', views.Ver_Paquetes_Cliente),
    path('Entrega/<int:id>', views.Ver_Paquetes_Entrega),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # path('admin-panel/', views.admin_panel, name='admin_panel'),
    # path('conductor-panel/', views.conductor_panel, name='conductor_panel'),
    # path('cliente-panel/', views.cliente_panel, name='cliente_panel'),
]