from django.shortcuts import render
from API.conection_bd import *
# Create your views here.

def create_paquete(request):
    clientes = obtener_cliente()
    bodegas = obtener_bodegas()

    if request.method == 'POST':
        try:
            remitente_id = int(request.POST['remitente'])
            remitente = CustomUser.objects.get(id=remitente_id)
            print(remitente)

            paquete = Paquete.objects.create(
                Remitente=remitente,
                Direccion=request.POST['direccion'],
                Origen=request.POST['origen'],
                Peso=request.POST['peso'],
                Dimensiones=request.POST['dimensiones'],
                Instrucciones_Entrega=request.POST.get('instrucciones', ''),
                Contenido=request.POST.get('contenido', ''),
                Estado=request.POST['estado'],
            )


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