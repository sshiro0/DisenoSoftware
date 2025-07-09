from .models import *

def obtener_paquetes():
    Paquetes = Paquete.objects.all()
    return Paquetes
def obtener_bodegas():
    bodegas = Bodegas_Paquetes
    return bodegas
def obtener_cliente():
    clientes = CustomUser.objects.filter(tipo_usuario='Cl')
    return clientes
def obtener_entregas():
    entregas = Entrega.objects.all()
    return entregas
def crear_paquete_bd(data):
    remitente = CustomUser.objects.get(id=data['remitente'])

    if remitente.tipo_usuario != 'Cl':
        raise ValueError("Solo se pueden asignar paquetes a usuarios tipo cliente")

    Paquete.objects.create(
        Remitente=remitente,
        Direccion=data['direccion'],
        Origen=data['origen'],
        Peso=data['peso'],
        Dimensiones=data['dimensiones'],
        Instrucciones_Entrega=data.get('instrucciones', ''),
        Contenido=data.get('contenido', ''),
        Estado=data['estado'],
        Destino=data.get('destino', '')  # si estás usando ese campo
    )

           