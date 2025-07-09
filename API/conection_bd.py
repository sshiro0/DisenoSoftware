from .models import *

def obtener_paquetes():
    Paquetes = Paquete.objects.all()
    return Paquetes

def obtener_entregas():
    entregas = Entrega.objects.all()
    return entregas