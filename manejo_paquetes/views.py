from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import *

from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, conductor_required, cliente_required
from django.core.cache import cache
from django.contrib import messages
from .forms import LoginForm



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

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    ip_address = request.META.get('REMOTE_ADDR')
    cache_key = f'login_attempts_{ip_address}'
    attempts = cache.get(cache_key, 0)
    
    if attempts >= 5:
        return render(request, 'auth/lockout.html')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.estado == 'B':
                messages.error(request, "Cuenta bloqueada")
                return redirect('login')
            
            cache.delete(cache_key)
            login(request, user)
            return redirect('dashboard')
        else:
            attempts += 1
            cache.set(cache_key, attempts, timeout=300)
            messages.error(request, f"Credenciales inválidas. Intentos restantes: {5 - attempts}")
    else:
        form = LoginForm()
    
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.tipo_usuario == 'Ad':
        return redirect('admin-dashboard')
    elif request.user.tipo_usuario == 'Co':
        return redirect('conductor-dashboard')
    return redirect('cliente-dashboard')

# Vistas para Admin
@method_decorator(admin_required, name='dispatch')
class AdminDashboardView(View):
    def get(self, request):
        return render(request, 'admin/dashboard.html')

# Vistas para Conductor
@method_decorator(conductor_required, name='dispatch')
class ConductorDashboardView(View):
    def get(self, request):
        return render(request, 'conductor/dashboard.html')

@method_decorator(conductor_required, name='dispatch')
class RutaOptimaView(View):
    def get(self, request):
        return render(request, 'conductor/ruta.html')

# Vistas para Cliente
@method_decorator(cliente_required, name='dispatch')
class ClienteDashboardView(View):
    def get(self, request):
        return render(request, 'cliente/dashboard.html')

@method_decorator(cliente_required, name='dispatch')
class PaquetesClienteView(View):
    def get(self, request):
        return render(request, 'cliente/paquetes.html')