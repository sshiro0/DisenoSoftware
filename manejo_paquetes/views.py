from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def hello(request):
    return HttpResponse("<h1>Hello World</h1>") 

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