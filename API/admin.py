from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Camion, Paquete

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
admin.site.register(Paquete)
