from .models import *

def obtener_paquetes():
    Paquetes = Paquete.objects.all()
    return Paquetes
def obtener_paquete_id(id):
    paquete = Paquete.objects.get(ID_paquete=id)
    return paquete
def obtener_bodegas():
    bodegas = Bodegas_Paquetes
    return bodegas
def obtener_cliente():
    clientes = CustomUser.objects.filter(tipo_usuario='Cl')
    return clientes
def obtener_conductores():
    conductores = CustomUser.objects.filter(tipo_usuario='Co')
    return conductores
def obtener_conductor_id(id_c):
    conductor = CustomUser.objects.get(id=id_c)if id_c else None
    return conductor
def obtener_camiones():
    camiones = Camion.objects.all()
    return camiones
def obtener_camiones_id(id_c):
    camion = Camion.objects.get(ID_camion=id_c)if id_c else None
    return camion
def obtener_entregas():
    entregas = Entrega.objects.all()
    return entregas
def obtener_entregas_c(conductor):
    entregas = Entrega.objects.filter(Conductor=conductor)
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
        Instrucciones_Entrega=data['instrucciones'],
        Contenido=data['contenido'],
        Estado=data['estado'],
        Destino=data.get('destino', '') # si estás usando ese campo
    )
def crear_entrega_bd(data):
    Entrega.objects.create(
            Destino=data['destino'],
            Conductor=data['conductor'],
            Camion=data['camion']
        )