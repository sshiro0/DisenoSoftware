from django.db import models
from django.contrib.auth.models import AbstractUser
from manejo_paquetes.utility.correos import enviar_correo
from django.utils.timezone import now
from location_field.models.plain import PlainLocationField
from django.utils import timezone


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
    ("R", "En reparto"),
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


class Paquete(models.Model):
    ID_paquete = models.BigAutoField(primary_key=True)
    Remitente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Destino = PlainLocationField(blank=True, null=True)
    Origen = models.CharField(max_length=150, choices= Bodegas_Paquetes, default=None)
    Peso = models.PositiveIntegerField()
    Dimensiones = models.CharField(max_length=2, choices=Dimensiones_Paquetes, default=None)
    Instrucciones_Entrega = models.CharField(max_length=200, default="")
    Contenido = models.CharField(max_length=80, default="")
    Estado = models.CharField(max_length=1, choices=Estados_paquetes, default='B')

    def save(self, *args, **kwargs):
        if self.Remitente and not self.Destino:
            self.Destino = self.Remitente.ID_cliente.direccion
        
        # Notificación de cambio de estado
        if self.pk:
            old = Paquete.objects.get(pk=self.pk)
            if old.Estado != self.Estado:
                self.notificar_cambio_estado()
        
        super().save(*args, **kwargs)
    
    def notificar_cambio_estado(self):
        estados_mensajes = {
            'B': "su paquete está en bodega",
            'R': "su paquete está en reparto",
            'E': "su paquete ha sido entregado"
        }
        mensaje = f"Actualización: {estados_mensajes.get(self.Estado, '')}"
        enviar_correo(
            self.Remitente.ID_cliente.email,
            "Estado de su paquete",
            mensaje
        )


class Entrega(models.Model):
    ID_entrega = models.BigAutoField(primary_key=True)
    Conductor = models.ForeignKey(Conductor, on_delete=models.SET_NULL, null=True, blank=True)
    Fecha_creacion = models.DateTimeField(default=timezone.now)
    Fecha_entrega = models.DateTimeField(null=True, blank=True)
    Estado = models.CharField(max_length=20, choices=[
            ('P', 'Pendiente'),
        ('E', 'En camino'),
        ('C', 'Completada'),
    ], default='P')

    # Relación muchos a muchos con Paquete usando un modelo intermedio
    paquetes = models.ManyToManyField(Paquete, through='Lista_Paquetes')

    def asignar_paquetes(self, paquetes_ids):
        """Asigna múltiples paquetes a esta entrega y actualiza su estado"""
        for paquete_id in paquetes_ids:
            paquete = Paquete.objects.get(pk=paquete_id)
            Lista_Paquetes.objects.create(entrega=self, paquete=paquete)
            paquete.Estado = 'R'  # Cambia estado a "Repartiendo"
            paquete.save()

    
    def completar_entrega(self):
        """Marca la entrega como completada y actualiza estados de paquetes"""
        self.Estado = 'C'
        self.Fecha_entrega = now()
        self.save()
        
        for paquete in self.paquetes.all():
            paquete.Estado = 'E'  # Cambia estado a "Entregado"
            paquete.save()

class Lista_Paquetes(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE)
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('entrega', 'paquete')  # Evita duplicados