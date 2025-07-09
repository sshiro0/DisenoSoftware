from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django import forms

# Si tu modelo CustomUser extiende AbstractUser, debes crear un admin personalizado:
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'tipo_usuario', 'estado', 'fecha_registro']
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('tipo_usuario', 'direccion', 'estado')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': ('tipo_usuario', 'direccion', 'estado')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Camion)

@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ('ID_paquete', 'Remitente', 'Destino', 'Estado')


class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['Destino']  # NO mostramos 'Lista_Paquetes', se llena sola

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mostrar solo direcciones únicas ya existentes en los paquetes
        direcciones = Paquete.objects.exclude(Direccion__isnull=True).exclude(Direccion__exact='') \
                                        .values_list('Direccion', flat=True).distinct()
        self.fields['Destino'].widget = forms.Select(choices=[(d, d) for d in direcciones])

admin.site.register(Entrega)

