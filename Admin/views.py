from django.shortcuts import render
from API.conection_bd import *
# Create your views here.

def create_paquete(request):
    clientes = obtener_cliente()
    bodegas = obtener_bodegas()

    if request.method == 'POST':
        try:

            data = {
                'remitente': int(request.POST['remitente']),
                'direccion': request.POST['direccion'],
                'origen': request.POST['origen'],
                'peso': request.POST['peso'],
                'dimensiones': request.POST['dimensiones'],
                'instrucciones': request.POST.get('instrucciones', ''),
                'contenido': request.POST.get('contenido', ''),
                'estado': request.POST['estado'],
                'destino': request.POST.get('destino', '')  # opcional
            }

            crear_paquete_bd(data)


        except (KeyError, ValueError, CustomUser.DoesNotExist) as e:
            return render(request, 'Admin/Admin_Paquete.html', {
                'clientes': clientes,
                'bodegas': bodegas,
                'error': 'Error al crear el paquete: ' + str(e)
            })

    return render(request, 'Admin/Admin_Paquete.html', {
        'clientes': clientes,
        'bodegas': bodegas
    })



def Admin(request):
    if request.method == 'POST':
        pass
    return render(request, 'Admin/Admin.html')