from django.db import models

# Create your models here.


Dimensiones_Paquetes = {
    "S" : "Pequeño",
    "M" : "Mediano",
    "L" : "Largo",
    "XL" : "Muy Largo",
}

Tipos_de_usuarios = {
    "Ad" : "Administrador", 
    "Co" : "Conductor",
    "Cl" : "Cliente",
}

Estados_paquetes = {
    "B" : "En bodega",
    "R" : "Repartiendo",
    "E" : "Entregado",
}

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


class Paquete(models.Model):

    ID_paquete = models.BigAutoField(primary_key=True)
    Remitente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Destino = models.CharField(max_length=150)
    Origen = models.CharField(max_length=150)
    Peso = models.SmallIntegerField()
    Dimensiones = models.CharField(max_length=2, choices=Dimensiones_Paquetes)
    Instrucciones_Entrega = models.CharField(max_length=200)
    Contenido = models.CharField(max_length=80)
    Estado = models.CharField(max_length=1, choices=Estados_paquetes)


class Conductor(models.Model):
    ID_conductor = models.BigAutoField(primary_key=True)
    



