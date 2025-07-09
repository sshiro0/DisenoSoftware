from .models import *
from manejo_paquetes.models import *

def obtener_paquetes():
    Paquetes = Paquete.objects.all()
    return Paquetes
def obtener_bodegas():
    bodegas = Bodegas_Paquetes
    return bodegas
def obtener_cliente():
    usuarios = Cliente.objects.all()
    return usuarios
def obtener_entregas():
    entregas = Entrega.objects.all()
    return entregas
def crear_paquete_BD(data):
        paquete = Paquete(
            Remitente=data['remitente'],
            Direccion=data['direccion'],
            Origen=data['origen'],
            Peso=data['peso'],
            Dimensiones=data['dimensiones'],
            Instrucciones=data['instrucciones'],
            Contenido=data['contenido'],
            Estado=data['estado']
        )
        Paquete.objects.create(
            Remitente=Cliente.objects.get(ID_cliente=data['remitente']),
            Direccion=paquete.Direccion,
            Origen=paquete.Origen,
            Peso=paquete.Peso,
            Dimensiones=paquete.Dimensiones,
            Instrucciones=paquete.Instrucciones,
            Contenido=paquete.Contenido,
            Estado=paquete.Estado
        )    