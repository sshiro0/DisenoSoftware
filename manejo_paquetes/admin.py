# from django.contrib import admin
# from .models import *
# from django import forms

# # Register your models here.

# @admin.register(Usuario)
# class UsuarioAdmin(admin.ModelAdmin):
#     list_display = ('ID_usuario', 'Nombre', 'Direccion', 'Tipo_Usuario')

# admin.site.register(Cliente)
# admin.site.register(Conductor)
# admin.site.register(Administrador)
# admin.site.register(Camion)

# @admin.register(Paquete)
# class PaqueteAdmin(admin.ModelAdmin):
#     list_display = ('ID_paquete', 'Remitente', 'Destino', 'Estado')

# class EntregaForm(forms.ModelForm):
#     class Meta:
#         model = Entrega
#         fields = ['Destino']  # NO mostramos 'Lista_Paquetes', se llena sola

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Mostrar solo direcciones únicas ya existentes en los paquetes
#         direcciones = Paquete.objects.exclude(Direccion__isnull=True).exclude(Direccion__exact='') \
#                                      .values_list('Direccion', flat=True).distinct()
#         self.fields['Destino'].widget = forms.Select(choices=[(d, d) for d in direcciones])

# admin.site.register(Entrega)

