from django.shortcuts import render, redirect
from API.conection_bd import *
# Create your views here.



def crear_usuario_general(request):
    if request.method == 'POST':
        try:
            tipo = request.POST['tipo_usuario']
            usuario = CustomUser.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                direccion=request.POST.get('direccion', ''),
                tipo_usuario=tipo
            )
            return render(request, 'Admin/Admin.html', {'exito': True})
        except Exception as e:
            return render(request, 'Admin/Crear_Conductor.html', {
                'error': 'Error al crear usuario: ' + str(e)
            })

    return render(request, 'Admin/Crear_Conductor.html')



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
                'destino': request.POST.get('destino', '')
            }

            crear_paquete_bd(data)
            return redirect('admin_login')


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


def crear_entrega(request):
    if request.method == 'POST':
        destino = request.POST.get('destino')
        conductor_id = request.POST.get('conductor')
        camion_id = request.POST.get('camion')

        conductor = obtener_conductor_id(conductor_id)
        camion = obtener_camiones_id(camion_id)

        data = {
            'destino': request.POST.get('destino'),
            'conductor': conductor,
            'camion': camion
        }
        crear_entrega_bd(data)
        return redirect('admin_login')  # o cambia al nombre que prefieras

    conductores = obtener_conductores()
    camiones = obtener_camiones()
    return render(request, 'Admin/crear_entrega.html', {
        'conductores': conductores,
        'camiones': camiones
    })