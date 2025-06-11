import openrouteservice as ors
import folium

#Inicializacion del cliente de ORS
client = ors.Client(key='5b3ce3597851110001cf6248782465e9b6b14ca9a036b6e4d110a193')

#Definimos la coordenadas de la/s sede/S
    #Formato [Longitud, Latitud] formato con el que trabaja ORS
sede_coords = [[-73.03852531674826,-36.82668501352285],
               [-73.01696915350173,-36.81958580497319]]

#El formato para ors es [Longitud, Latitud], lo opuesto a la mayoria de los sistemas de coordenadas, motivo por el cual se invierten

#Definimos el grupo de coordenadas de destino
dest_coords = [[-73.04391854071059, -36.818045789079320],
               [-73.06106239057411, -36.821266818502340],
               [-73.05582684156164, -36.817989805917960],
               [-73.05884027705054, -36.829970488752280],
               [-73.05007995584482, -36.833498355954610],
               [-73.045402982504, -36.82445072087983000],
               [-73.03849837824572, -36.824133177028166],
               [-73.0416923969898, -36.8128609590356100],]

#Inicializacion del mapa (Idealmente se crea el mapa en la coordenada de la sede)
map = folium.Map(location = list(reversed([-73.04391854071059, -36.81804578907932])), tiles="cartodbpositron", zoom_start=13)



#Visualizacion de las sedes en el mapa
for coord in sede_coords:
    folium.Marker(location=list(reversed(coord)), icon=folium.Icon(color="red")).add_to(map)


#Se crean los vehiculos, por simplicidad hay un vehiculo por sede, cada uno con una capacidad de 3

#Alternativa para crear tantos vehiculos como sedes hayan
#vehicles = [ors.optimization.Vehicle(id=index, profile='driving-car', start=cord, end=cord, capacity=[5]) for index, cord in enumerate(sede_coords)]

#Tambien se pueden crear vehiculos uno por uno
vehicles = [
    ors.optimization.Vehicle(id=0,
                             profile='driving-car', 
                             start = sede_coords[0],
                             end = sede_coords[0], 
                             capacity = [4]), #Capacidad del vehiculo (se entiende como la cantidad de paquetes que puede llevar)
                                              #Pero en este caso se entenderá como la cantidad de entregas que puede realizar

    ors.optimization.Vehicle(id=1, 
                             profile='driving-car', 
                             start = sede_coords[1], 
                             end = sede_coords[1], 
                             capacity = [4]),
]

#Se crean los trabajos, que corresponden a las entregas que se van a realizar
    #En este caso "amount" corresponde a la cantidad de paquetes que se van a entregar, pero de deja por defecto en 1 para
    #pues cada trabajo corresponde a una entrega
jobs = [ors.optimization.Job(id=index, location=coords, amount=[1]) for index, coords in enumerate(dest_coords)]

optimized = client.optimization(jobs=jobs, vehicles=vehicles, geometry=True)

colors = ['green', 'orange','blue', 'yellow']

for route in optimized['routes']:
    folium.PolyLine(locations=[list(reversed(coords)) for coords in ors.convert.decode_polyline(route['geometry'])['coordinates']], color=colors[route['vehicle']]).add_to(map)


########CREACION DE MARCADORES PARA RUTAS OPTIMIZADAS########
jobs_order = {} #Diccionarios para almecenar el orden de los trabajos

#Recorremos la rutas optimizadas
for route in optimized['routes']:
    vehicle_id = route['vehicle']
    steps = route['steps']

    #Inicializacion en 1 debido a que se comienza desde la primera entrega
    order = 1
    #Recorremos los pasos de la ruta
    for step in steps:
        if step['type'] == 'job':
            job_id = step['id']
            jobs_order[job_id] = {
                'order' : order,
                'vehicle_id' : vehicle_id
            }
            order +=1
    
#Creamos los marcadores para las entregas
for index, coord in enumerate(dest_coords):
    info = jobs_order.get(index)
    if(info):
        popup_text = f"Entrega #{info['order']} (Vehículo {info['vehicle_id']})"
    else:
        popup_text = "Entrega no asignada"

    folium.Marker(location=list(reversed(coord)),
                  popup=popup_text,
                  icon=folium.Icon(color='blue')).add_to(map)



#Guardado del mapa en un archivo HTML
map.save('map.html')