from django.shortcuts import render
from API.conection_bd import *
# Create your views here.

def create_paquete(request):
    clientes = obtener_cliente()
    bodegas = obtener_bodegas()
    print(bodegas)
    if request.method == 'POST':
        data = {
            'remitente': request.POST['remitente'],
            'direccion': request.POST['direccion'],
            'origen': request.POST['origen'],
            'peso': request.POST['peso'],
            'dimensiones': request.POST['dimensiones'],
            'instrucciones': request.POST['instrucciones'],
            'contenido': request.POST['contenido'],
            'estado': request.POST['estado'],
        }   
        crear_paquete_BD(data)

    return render(request, 'Admin_Paquete.html', {'exito': True, 'clientes': clientes, 'bodegas': bodegas})


def Admin(request):
    if request.method == 'POST':
        pass
    return render(request, 'Admin.html')