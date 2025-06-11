from django.db import models
from utility.Correos import enviar_correo
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

class Usuario(models.Model):
    ID_usuario = models.BigAutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    Correo = models.EmailField()
    Contrasena = models.CharField(max_length=20)
    Direccion = models.CharField(max_length=150)
    Tipo_Usuario = models.CharField(max_length=2 , choices=Tipos_de_usuarios)
    Fecha_Registro = models.DateField()
    Estado = models.CharField()


class Cliente(models.Model):
    ID_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, primary_key=True)


class Administrador(models.Model):
    ID_admin = models.ForeignKey(Usuario, on_delete=models.CASCADE, primary_key=True)


class Conductor(models.Model):
    ID_conductor = models.ForeignKey(Usuario, on_delete=models.CASCADE, primary_key=True)


class Camion(models.Model):
    ID_camion = models.BigAutoField(primary_key=True)

class Envio(models.Model):
    ID_envio = models.BigAutoField(primary_key=True)


class Paquete(models.Model):
    ID_paquete = models.BigAutoField(primary_key=True)
    Remitente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Destino = models.CharField(max_length=150, default=None, blank=True, null=True)
    Origen = models.CharField(max_length=150, choices= Bodegas_Paquetes, default=None)
    Peso = models.PositiveIntegerField()
    Dimensiones = models.CharField(max_length=2, choices=Dimensiones_Paquetes, default=None)
    Instrucciones_Entrega = models.CharField(max_length=200, default="")
    Contenido = models.CharField(max_length=80, default="")
    Estado = models.CharField(max_length=1, choices=Estados_paquetes, default=None)
    Envio = models.ForeignKey(Envio, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.Remitente and not self.Destino:
            self.Destino = self.Remitente.ID_cliente.Direccion

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
    Conductor = models.ForeignKey(Conductor, on_delete=models.SET_NULL, null=True, blank=True)
    Camion = models.ForeignKey(Camion, on_delete=models.SET_NULL, null=True, blank=True)
    Ruta = models.ForeignKey(Ruta, on_delete=models.SET_NULL, null=True, blank=True)
    Lista_Paquetes = models.ManyToManyField(Paquete)


class Notificacion(models.Model):
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)





