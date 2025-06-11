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

def Ver_Paquetes_Entrega(request):
    entregas = Entrega.objects.all()
    paquetes = Paquete.objects.all()
    return render(request, 'Paquetes_entrega.html', {
        'entregas' : entregas,
        'paquetes' : paquetes,
    })