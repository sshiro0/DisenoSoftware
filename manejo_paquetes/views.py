from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from .models import *
from .utility.direcciones import map_route

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


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

def Ver_ruta(request):
    entregas = Entrega.objects.all()
    paquetes = Paquete.objects.all()
    nombres_mapas = []
    for entrega in entregas: 
        paquetes_direccion = Paquete.objects.filter(Direccion = entrega.Destino)
        coordenadas = [tuple(map(float, paquete.Destino.split(','))) for paquete in paquetes_direccion]
        nombremapa = f"mapa_entrega_{entrega.id}" 
        nombres_mapas.append(f"{nombremapa}.html")
        map_route(dest_coords=list(reversed(coordenadas)), sede_coords=Bodegas_cords, nombre_mapa=nombremapa)
    return render(request, 'Rutas_entregas.html',{
        'mapas' : nombres_mapas,
    })

def login_view(request):
    
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        user = authenticate(request, correo=correo, contrasena=contrasena)
        
        try:
            user = Usuario.objects.get(Correo=correo)
            
            # Verificar contraseña (sin encriptación por ahora)
            if user.Contrasena == contrasena:
                request.session['user_id'] = user.ID_usuario
                request.session['tipo_usuario'] = user.Tipo_Usuario
                return redirect_to_dashboard(user)
            else:
                messages.error(request, 'Correo o contraseña incorrectos')
        except Usuario.DoesNotExist:
            messages.error(request, 'Correo o contraseña incorrectos')
    
    return render(request, 'login.html')


def redirect_to_dashboard(user):
    """Función auxiliar para redireccionar según tipo de usuario"""
    if user.tipo_usuario == 'Ad':
        return redirect('/admin/')
    elif user.tipo_usuario == 'Co':
        return redirect('dashboard_conductor')
    elif user.tipo_usuario == 'Cl':
        return redirect('dashboard_cliente')
    return redirect('login')

def logout_view(request):
    # Limpiar la sesión
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'tipo_usuario' in request.session:
        del request.session['tipo_usuario']
    return redirect('login')

class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            try:
                request.user = Usuario.objects.get(ID_usuario=user_id)
            except Usuario.DoesNotExist:
                request.user = None
        else:
            request.user = None
        
        response = self.get_response(request)
        return response

# Decorador para verificar tipo de usuario
def user_type_required(*allowed_types):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if not request.session.get('user_id'):
                return redirect('login')
                
            try:
                user = Usuario.objects.get(ID_usuario=request.session['user_id'])
                if user.Tipo_Usuario not in allowed_types:
                    return HttpResponseForbidden("No tienes permiso para acceder a esta página")
                return view_func(request, *args, **kwargs)
            except Usuario.DoesNotExist:
                return redirect('login')
        return wrapped_view
    return decorator

# Vistas protegidas
@user_type_required('Cl')
def dashboard_cliente(request):
    return render(request, 'dashboard-cliente.html')

@user_type_required('Co')
def dashboard_conductor(request):
    return render(request, 'dashboard-conductor.html')

# Añadir después vistas según tipo de usuario con Ruta_entrega.html, Paquetes_Cliente.html, Paquetes_entrega.html