from django.shortcuts import render
from API.conection_bd import *
from manejo_paquetes.utility.direcciones import map_route

def Ver_Paquetes_Entrega(request):
    entregas = obtener_entregas()
    paquetes = obtener_paquetes()
    return render(request, 'Conductor/Paquetes_entrega.html', {
        'entregas' : entregas,
        'paquetes' : paquetes,
    })

def Ver_ruta(request):
    entregas = obtener_entregas()
    paquetes = obtener_paquetes()
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
        coordenadas.clear()
    return render(request, 'Conductor/Rutas_entregas.html',{
        'mapas' : nombres_mapas,
    })
