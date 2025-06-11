from django.contrib import admin
from .models import *
from django import forms

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_nombre_completo', 'get_direccion', 'get_tipo_usuario_display')
    
    def get_nombre_completo(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_nombre_completo.short_description = 'Nombre'
    
    def get_direccion(self, obj):
        return obj.direccion
    get_direccion.short_description = 'Direccion'
    
    def get_tipo_usuario_display(self, obj):
        return obj.get_tipo_usuario_display()
    get_tipo_usuario_display.short_description = 'Tipo_Usuario'

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('ID_cliente',)

@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = ('ID_conductor', 'Camion')

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('ID_admin',)

@admin.register(Camion)
class CamionAdmin(admin.ModelAdmin):
    list_display = ('ID_camion', 'Patente')

@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ('ID_paquete', 'get_remitente', 'get_destino', 'get_estado_display')
    
    def get_remitente(self, obj):
        return obj.Remitente.ID_cliente.get_full_name()
    get_remitente.short_description = 'Remitente'
    
    def get_destino(self, obj):
        return obj.Destino if obj.Destino else "Bodega"
    get_destino.short_description = 'Destino'
    
    def get_estado_display(self, obj):
        return obj.get_Estado_display()
    get_estado_display.short_description = 'Estado'

class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['Destino']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        direcciones = Paquete.objects.exclude(Direccion__isnull=True).exclude(Direccion__exact='') \
                                   .values_list('Direccion', flat=True).distinct()
        self.fields['Destino'].widget = forms.Select(choices=[(d, d) for d in direcciones])

@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    form = EntregaForm
    list_display = ('id', 'Destino')