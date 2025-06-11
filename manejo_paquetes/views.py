from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .utility.direcciones import map_route

# Create your views here.

def hello(request):
    return HttpResponse("<h1>Hello World</h1>") 

def Ver_Paquetes_Cliente(request, id):
    Paquetes = Paquete.objects.all()
    return render(request, 'Paquetes_Cliente.html',{
        'paquetes' : Paquetes,
        'ID' : id
    })

def Ver_Paquetes_Entrega(request):
    entregas = Entrega.objects.all()
    paquetes = Paquete.objects.all()
    return render(request, 'Paquetes_entrega.html', {
        'entregas' : entregas,
        'paquetes' : paquetes,
    })

def Ver_ruta(request):
    entregas = Entrega.objects.all()
    paquetes = Paquete.objects.all()
    nombres_mapas = []
    for entrega in entregas: 
        paquetes_direccion = Paquete.objects.filter(Direccion = entrega.Destino)
        coordenadas = [tuple(map(float, paquete.Destino.split(','))) for paquete in paquetes_direccion]
        nombremapa = f"mapa_entrega_{entrega.id}" 
        nombres_mapas.append(f"{nombremapa}.html")
        map_route(dest_coords=list(reversed(coordenadas)), sede_coords=Bodegas_cords, nombre_mapa=nombremapa)
    return render(request, 'Rutas_entregas.html',{
        'mapas' : nombres_mapas,
    })
