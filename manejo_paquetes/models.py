from django.db import models
from django.contrib.auth.models import AbstractUser
from manejo_paquetes.utility.Correos import enviar_correo
from django.utils.timezone import now
from location_field.models.plain import PlainLocationField
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
    ("B1", "Edmundo Larenas 160 Concepcion"),
    ("B2", "Maipú 2120 Concepcion"),
    ("B3", "Camilo Henríquez 2345 Concepcion"),
    ("B4", "Arturo Prat 900 Concepcion"),
]

class Usuario(AbstractUser):
    TIPOS_USUARIO = [
        ("Ad", "Administrador"),
        ("Co", "Conductor"),
        ("Cl", "Cliente"),
    ]
    
    ESTADOS = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ('B', 'Bloqueado'),
    ]

    direccion = models.CharField(max_length=150)
    tipo_usuario = models.CharField(max_length=2, choices=TIPOS_USUARIO)
    fecha_registro = models.DateField(default=now)
    estado = models.CharField(max_length=20, default='A')
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_tipo_usuario_display()})"



class Cliente(models.Model):
    ID_cliente = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)


class Administrador(models.Model):
    ID_admin = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)


class Camion(models.Model):
    ID_camion = models.BigAutoField(primary_key=True)
    Patente = models.CharField(max_length=6, null=True, default=None, blank=True)

class Conductor(models.Model):
    ID_conductor = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    Camion = models.ForeignKey(Camion, null=True, on_delete=models.SET_NULL)


class Envio(models.Model):
    ID_envio = models.BigAutoField(primary_key=True)


class Paquete(models.Model):
    ID_paquete = models.BigAutoField(primary_key=True)
    Remitente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Destino = PlainLocationField(blank=True, null=True)
    Origen = models.CharField(max_length=150, choices= Bodegas_Paquetes, default=None)
    Peso = models.PositiveIntegerField()
    Dimensiones = models.CharField(max_length=2, choices=Dimensiones_Paquetes, default=None)
    Instrucciones_Entrega = models.CharField(max_length=200, default="")
    Contenido = models.CharField(max_length=80, default="")
    Estado = models.CharField(max_length=1, choices=Estados_paquetes, default=None)

    def save(self, *args, **kwargs):
        if self.Remitente and not self.Destino:
            self.Destino = self.Remitente.ID_cliente.Direccion

        #sistema observer, que al momento de cambiar el estado 
        # de un paquete, se le avisa al cliente 
        if self.pk:
            old = Paquete.objects.get(pk=self.pk)
            if old.Estado != self.Estado:
                Correo = self.Remitente.ID_cliente.Correo
                if self.Estado == "E":
                    mensaje_correo = "Su paquete a sido entregado"
                elif self.Estado == "R":
                    mensaje_correo = "Su paquete está siendo repartido"
                else:
                    mensaje_correo = "Su paquete está en bodega y pronto será repartido"
                
                enviar_correo(correo_destinatario=Correo, 
                              asunto="Se actualizo el estado de su paquete",
                              mensaje=mensaje_correo)
                
        super().save(*args, **kwargs)

    


class Ruta(models.Model):
    ID_ruta = models.BigAutoField(primary_key=True)


class Entrega(models.Model):
    ID_entrega = models.BigAutoField(primary_key=True)
    Destino = models.CharField(max_length=150, default=None, blank=True, null=True)
    #Destino es la direccion en palabras, que debemos pasar a cords

    # Relación muchos a muchos con Paquete usando un modelo intermedio
    paquetes = models.ManyToManyField(Paquete, through='Lista_Paquetes')

    def save(self, *args, **kwargs):
        if not self.destino and self.pk is None:
            # Solo si aún no tiene destino definido
            primer_paquete = self.paquetes.first()
            if primer_paquete:
                self.destino = primer_paquete.destino
        super().save(*args, **kwargs)

class Lista_Paquetes(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE)
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)






