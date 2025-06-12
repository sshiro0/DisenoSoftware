from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .utility.direcciones import map_route

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        contrasena = request.POST['contrasena']
        try:
            usuario = Usuario.objects.filter(Correo=correo, Contrasena=contrasena).first()
        
            if usuario is None:
                return render(request, 'login.html')

            if Cliente.objects.filter(ID_cliente__ID_usuario=usuario.ID_usuario).exists():
                return redirect('ver_paquetes_cliente', id=usuario.ID_usuario)

            if Conductor.objects.filter(ID_conductor__ID_usuario=usuario.ID_usuario).exists():
                return redirect('ver_entregas')

            if Administrador.objects.filter(ID_admin__ID_usuario=usuario.ID_usuario).exists():
                return redirect('/admin/')  # o tu vista personalizada: redirect('panel_admin')

            else:
                messages.error(request, 'Tu cuenta no está asignada como cliente, conductor ni administrador.')

        except Usuario.DoesNotExist:
            messages.error(request, 'Correo o contraseña incorrectos.')

    return render(request, 'login.html')

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
    return render(request, 'Rutas_entregas.html',{
        'mapas' : nombres_mapas,
    })
