from django.db import models
from manejo_paquetes.utility.Correos import enviar_correo
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password
from location_field.models.plain import PlainLocationField


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

Bodegas_cords = [
    (-73.038343, -36.82970312988858),
    (-73.03169734825777, -36.81604496647257),
    (-73.03608766175144, -36.81099039611668),
    (-73.06113404825716, -36.82581091203825),
]

class Usuario(models.Model):
    ID_usuario = models.BigAutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    Correo = models.EmailField()
    Contrasena = models.CharField(max_length=20)
    Direccion = models.CharField(max_length=150)
    Tipo_Usuario = models.CharField(max_length=2 , choices=Tipos_de_usuarios)
    Fecha_Registro = models.DateField(default=None, blank=True, null=True)
    Estado = models.CharField()

    def set_password(self, raw_password):
        self.Contrasena = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.Contrasena)

    def save(self, *args, **kwargs):
        if self.Fecha_Registro is None:
            self.Fecha_Registro = now().date()
        super().save(*args, **kwargs)


class Cliente(models.Model):
    ID_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, primary_key=True)


class Administrador(models.Model):
    ID_admin = models.ForeignKey(Usuario, on_delete=models.CASCADE, primary_key=True)


class Camion(models.Model):
    ID_camion = models.BigAutoField(primary_key=True)
    Patente = models.CharField(max_length=6, null=True, default=None, blank=True)

class Conductor(models.Model):
    ID_conductor = models.ForeignKey(Usuario, on_delete=models.CASCADE, primary_key=True)
    Camion = models.ForeignKey(Camion, null=True, on_delete=models.SET_NULL)


class Paquete(models.Model):
    ID_paquete = models.BigAutoField(primary_key=True)
    Remitente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Direccion = models.CharField(max_length=150, default=None, null=True, blank=True)
    Destino = PlainLocationField(blank=True, null=True)
    Origen = models.CharField(max_length=150, choices= Bodegas_Paquetes, default=None)
    Peso = models.PositiveIntegerField()
    Dimensiones = models.CharField(max_length=2, choices=Dimensiones_Paquetes, default=None)
    Instrucciones_Entrega = models.CharField(max_length=200, default="")
    Contenido = models.CharField(max_length=80, default="")
    Estado = models.CharField(max_length=1, choices=Estados_paquetes, default=None)

    def save(self, *args, **kwargs):
        if self.Remitente and not self.Direccion:
            self.Direccion = self.Remitente.ID_cliente.Direccion
        #sistema observer, que al momento de cambiar el estado 
        # de un paquete, se le avisa al cliente 
        if self.pk:
            old = Paquete.objects.get(pk=self.pk)
            if old.Estado != self.Estado:
                Correo = self.Remitente.ID_cliente.Correo
                if self.Estado == "E":
                    mensaje_correo = "Su paquete ha sido entregado"
                elif self.Estado == "R":
                    mensaje_correo = "Su paquete está siendo repartido"
                else:
                    mensaje_correo = "Su paquete está en bodega y pronto será repartido"
                
                enviar_correo(correo_destinatario=Correo, 
                              asunto="Se actualizo el estado de su paquete",
                              mensaje=mensaje_correo)
                
        super().save(*args, **kwargs)


class Entrega(models.Model):
    Destino = models.CharField(max_length=150, default=None, blank=True, null=True)
            

