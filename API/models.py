from django.db import models
from django.conf import settings
from manejo_paquetes.utility.Correos import enviar_correo
from django.utils.timezone import now
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import User, AbstractUser
# Create your models here.


Dimensiones_Paquetes = [
    ("S", "Pequeño"),
    ("M", "Mediano"),
    ("L", "Largo"),
    ("XL", "Muy Largo"),
]

Tipos_de_usuarios = [
    ("Ad", "Administrador"),
    ("Co", "Conductor"),
    ("Cl", "Cliente"),
]

Estados_paquetes = [
    ("B", "En bodega"),
    ("R", "Repartiendo"),
    ("E", "Entregado"),
]

Bodegas_Paquetes = [
    ("B1", "Edmundo Larenas 160 Concepcion")
]

Bodegas_cords = [
    (-73.038343, -36.82970312988858)
]



class CustomUser(AbstractUser):
    tipo_usuario = models.CharField(max_length=2, choices=Tipos_de_usuarios) 
    direccion = models.CharField(max_length=150, blank=True, null=True)#opcional
    fecha_registro = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, default="activo")



class Camion(models.Model):
    ID_camion = models.BigAutoField(primary_key=True)
    Patente = models.CharField(max_length=6, null=True, default=None, blank=True)

class Paquete(models.Model):
    ID_paquete = models.BigAutoField(primary_key=True)
    Remitente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ahora es un User
    Direccion = models.CharField(max_length=150, default=None, null=True, blank=True)
    Destino = PlainLocationField(blank=True, null=True)
    Origen = models.CharField(max_length=150, choices=Bodegas_Paquetes, default=None)
    Peso = models.PositiveIntegerField()
    Dimensiones = models.CharField(max_length=2, choices=Dimensiones_Paquetes, default=None)
    Instrucciones_Entrega = models.CharField(max_length=200, default="", blank=True)
    Contenido = models.CharField(max_length=80, default="", blank=True)
    Estado = models.CharField(max_length=1, choices=Estados_paquetes, default=None)

    def save(self, *args, **kwargs):
    # Establecer dirección si no está definida
        if self.Remitente and not self.Direccion:
            self.Direccion = self.Remitente.direccion  # ahora está en el CustomUser directamente

        # Validar que el remitente sea un cliente
        if self.Remitente.tipo_usuario.strip().upper() != 'CL':
            raise ValueError("El remitente debe ser un usuario con tipo 'Cliente'")

        # Verificar cambio de estado y notificar
        if self.pk:
            old = Paquete.objects.get(pk=self.pk)
            if old.Estado != self.Estado:
                correo = self.Remitente.email  
                if self.Estado == "E":
                    mensaje_correo = "Su paquete ha sido entregado"
                elif self.Estado == "R":
                    mensaje_correo = "Su paquete está siendo repartido"
                else:
                    mensaje_correo = "Su paquete está en bodega y pronto será repartido"

                enviar_correo(
                    correo_destinatario=correo,
                    asunto="Se actualizó el estado de su paquete",
                    mensaje=mensaje_correo
                )

        super().save(*args, **kwargs)


class Entrega(models.Model):
    Destino = models.CharField(max_length=150, default=None, blank=True, null=True)
            

