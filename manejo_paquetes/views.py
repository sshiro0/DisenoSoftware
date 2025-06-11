from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
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
        messages.error(request, "Demasiados intentos fallidos. Intente más tarde")
        return render(request, 'manejo_paquetes/auth/lockout.html')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.estado == 'B':
                    messages.error(request, "Su cuenta está bloqueada.")
                    return redirect('login')
                
                cache.delete(cache_key)
                login(request, user)
                return redirect('dashboard')
            
            else:
                attempts += 1
                cache.set(cache_key, attempts, timeout=30)  
                remaining = 5 - attempts
                messages.error(request, f"Credenciales incorrectas. Intentos restantes: {remaining}")
        else:
            attempts += 1
            cache.set(cache_key, attempts, timeout=30)
            remaining = 5 - attempts
            messages.error(request, f"Formulario inválido. Intentos restantes: {remaining}")
    else:
        form = LoginForm()
    
    return render(request, 'auth/login.html', {'form': form, 'attempts_remaining': 5 - attempts})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    if user.tipo_usuario == 'Ad':
        return render(request, 'dashboard/admin.html')
    elif user.tipo_usuario == 'Co':
        return render(request, 'dashboard/conductor.html')
    else:
        return render(request, 'dashboard/cliente.html')
    