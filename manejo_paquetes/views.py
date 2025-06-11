from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .utility.correos import enviar_correo
from .utility.direcciones import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, conductor_required, cliente_required
from django.utils.decorators import method_decorator
from django.views import View


from .forms import LoginForm

# Vista Dashboard Admin
@admin_required
def admin_dashboard(request):
    # Todos los paquetes con filtros
    estado = request.GET.get('estado', '')
    bodega = request.GET.get('bodega', '')
    
    paquetes = Paquete.objects.all()
    
    if estado:
        paquetes = paquetes.filter(Estado=estado)
    if bodega:
        paquetes = paquetes.filter(Origen=bodega)
    
    context = {
        'paquetes': paquetes,
        'estados': dict(Paquete.Estados_paquetes),
        'bodegas': dict(Paquete.Bodegas_Paquetes),
        'filtro_estado': estado,
        'filtro_bodega': bodega
    }
    return render(request, 'admin/dashboard.html', context)

# Vista Dashboard Cliente
@cliente_required
def cliente_dashboard(request):
    
    # Solo paquetes del cliente logueado
    paquetes = Paquete.objects.filter(Remitente__ID_cliente=request.user)
    
    context = {
        'paquetes': paquetes,
        'estados': dict(Paquete.Estados_paquetes)
    }
    return render(request, 'cliente/dashboard.html', context)

# Vista Dashboard Conductor
@conductor_required
def conductor_dashboard(request):
    # Envios asignados al conductor
    conductor = request.user.conductor
    entregas = Entrega.objects.filter(
        Q(paquetes__Estado='R') & 
        Q(paquetes__Conductor_asignado=conductor)
    )
    context = {
        'entregas': entregas.distinct()
    }
    return render(request, 'conductor/dashboard.html', context)

    # Vista Ruta Óptima
@conductor_required
def ruta_optima(request, entrega_id):
    entrega = Entrega.objects.get(pk=entrega_id)
    paquetes = entrega.paquetes.all()
    
    # Convertir direcciones a coordenadas (necesitarás implementar esto)
    dest_coords = [obtener_coordenadas(p.Destino) for p in paquetes]
    sede_coords = [obtener_coordenadas_bodega(paquetes[0].Origen)] if paquetes else []
    
    # Generar mapa de ruta
    map_route(dest_coords, sede_coords)
    
    # En producción, deberías guardar el mapa con un nombre único y servir el archivo
    with open('map.html', 'r') as f:
        mapa_html = f.read()
    
    context = {
        'entrega': entrega,
        'paquetes': paquetes,
        'mapa_html': mapa_html
    }
    return render(request, 'conductor/ruta.html', context)

# Función auxiliar para notificar cambios de estado
def notificar_cambio_estado(paquete, nuevo_estado):
    if paquete.Estado != nuevo_estado:
        mensajes = {
            'B': "su paquete está en bodega",
            'R': "su paquete está en reparto",
            'E': "su paquete ha sido entregado"
        }
        mensaje = f"Actualización: {mensajes[nuevo_estado]}"
        enviar_correo(
            paquete.Remitente.ID_cliente.email,
            "Estado de su paquete",
            mensaje
        )


@admin_required
def crear_entrega(request):
    if request.method == 'POST':
        conductor_id = request.POST.get('conductor')
        paquetes_ids = request.POST.getlist('paquetes')
        
        conductor = Conductor.objects.get(pk=conductor_id)
        entrega = Entrega.objects.create(Conductor=conductor)
        entrega.asignar_paquetes(paquetes_ids)
        
        messages.success(request, "Entrega creada y paquetes asignados")
        return redirect('admin-dashboard')
    
    # GET request
    conductores = Conductor.objects.all()
    paquetes = Paquete.objects.filter(Estado='B')  # Solo paquetes en bodega
    return render(request, 'admin/crear_entrega.html', {
        'conductores': conductores,
        'paquetes': paquetes
    })

@conductor_required
def completar_entrega(request, entrega_id):
    entrega = Entrega.objects.get(pk=entrega_id)
    
    if request.method == 'POST' and entrega.Conductor.ID_conductor == request.user:
        entrega.completar_entrega()
        messages.success(request, "Entrega marcada como completada")
        return redirect('conductor-dashboard')
    
    return render(request, 'conductor/confirmar_entrega.html', {
        'entrega': entrega
    })

#def Ver_Paquetes_Cliente(request, id):
#    Paquetes = Paquete.objects.all()
#    return render(request, 'Paquetes_Cliente.html',{
#        'paquetes' : Paquetes,
#        'ID' : id
#    })

# def Ver_Paquetes_Entrega(request, id):
 #   entrega = Entrega.objects.get(id=id)
 #   if entrega.exists():
 #       paquetes = entrega.Lista_Paquetes.all()
 #   else:
 #       entrega = None
 #       paquetes = None
 #   return render(request, 'Paquetes_entrega.html', {
 #       'Entrega' : entrega,
 #       'Paquetes' : paquetes
 #   })

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