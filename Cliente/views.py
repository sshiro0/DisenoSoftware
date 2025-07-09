from django.shortcuts import render
from  API.conection_bd import *

def Ver_Paquetes_Cliente(request, id):
    Paquetes = obtener_paquetes()
    return render(request, 'Cliente/Paquetes_Cliente.html',{
        'paquetes' : Paquetes,
        'ID' : id
    })

# Create your views here.
