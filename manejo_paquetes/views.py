from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .utility.Correos import enviar_correo
from .utility.direcciones import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, conductor_required, cliente_required
from django.utils.decorators import method_decorator
from django.views import View
from django.core.cache import cache

from .forms import LoginForm


def Ver_Paquetes_Cliente(request, id):
    Paquetes = Paquete.objects.all()
    return render(request, 'Paquetes_Cliente.html',{
        'paquetes' : Paquetes,
        'ID' : id
    })

def Ver_Paquetes_Entrega(request, id):
   entrega = Entrega.objects.get(id=id)
   if entrega.exists():
       paquetes = entrega.Lista_Paquetes.all()
   else:
       entrega = None
       paquetes = None
   return render(request, 'Paquetes_entrega.html', {
       'Entrega' : entrega,
       'Paquetes' : paquetes
   })

def Ver_ruta(request):
    entregas = Entrega.objects.all()
    paquetes = Paquete.objects.all()
    nombres_mapas = []
    coordenadas = []
    for entrega in entregas: 
        paquetes_direccion = Paquete.objects.filter(Direccion = entrega.Destino)
        for paquete in paquetes_direccion:
            lat_str, lon_str = paquete.Destino.split(',')
            lat, lon = float(lat_str), float(lon_str)
            coordenadas.append((lon, lat))
        nombremapa = f"mapa_entrega_{entrega.id}" 
        nombres_mapas.append(f"{nombremapa}.html")
        map_route(dest_coords=coordenadas, sede_coords=Bodegas_cords, nombre_mapa=nombremapa)
        print(nombres_mapas)
    return render(request, 'Rutas_entregas.html',{
        'mapas' : nombres_mapas,
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard_redirect')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_redirect(request):
    if request.user.tipo_usuario == 'Cl':
        return redirect('dashboard_cliente')
    elif request.user.tipo_usuario == 'Co':
        return redirect('dashboard_conductor')
    elif request.user.tipo_usuario == 'Ad':
        return redirect('/admin/')

@login_required
def dashboard_cliente(request):
    return render(request, 'dashboard_cliente.html')

@login_required
def dashboard_conductor(request):
    return render(request, 'dashboard_conductor.html')