from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

def hello(request):
    return HttpResponse("<h1>Hello World</h1>") 

def pagina_inicio(request):
    return render(request, 'Pagina_inicial.html')

def pagina_camionero(request):
    return render(request, 'Pagina_Camionero.html')

def pagina_cliente(request):
    return render(request, 'Pagina_Cliente.html')



def Ver_Paquetes_Cliente(request, id):
    Paquetes = Paquete.objects.all()
    return render(request, 'Paquetes_Cliente.html',{
        'paquetes' : Paquetes,
        'ID' : id
    })