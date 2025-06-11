import openrouteservice as ors
import folium

def map_route(dest_coords:list, sede_coords:list):

    #Inicializacion del cliente de ORS
    client = ors.Client(key='5b3ce3597851110001cf6248782465e9b6b14ca9a036b6e4d110a193')



    #Inicializacion del mapa (Idealmente se crea el mapa en la coordenada de la sede)
    map = folium.Map(location = list(reversed(sede_coords[0])), tiles="cartodbpositron", zoom_start=13)



    #Visualizacion de las sedes en el mapa
    for coord in sede_coords:
        folium.Marker(location=list(reversed(coord)), icon=folium.Icon(color="red")).add_to(map)


    #Se crean los vehiculos, por simplicidad hay un vehiculo por sede, cada uno con una capacidad de 5

    #Creamos tantos vehiculos como sedes hayan sido ingresadas
    vehicles = [ors.optimization.Vehicle(id=index, profile='driving-car', start=cord, end=cord, capacity=[5]) for index, cord in enumerate(sede_coords)]

    #La capacidad del vehiculo (se entiende como la cantidad de paquetes que puede llevar) pero en este caso se entenderá como la cantidad de entregas que puede realizar
   
    #Se crean los trabajos, que corresponden a las entregas que se van a realizar
        #En este caso "amount" corresponde a la cantidad de paquetes que se van a entregar, pero de deja por defecto en 1 para
        #pues cada trabajo corresponde a una entrega
    jobs = [ors.optimization.Job(id=index, location=coords, amount=[1]) for index, coords in enumerate(dest_coords)]

    optimized = client.optimization(jobs=jobs, vehicles=vehicles, geometry=True)

    colors = ['green', 'orange','blue', 'yellow']

    for route in optimized['routes']:
        folium.PolyLine(locations=[list(reversed(coords)) for coords in ors.convert.decode_polyline(route['geometry'])['coordinates']], color=colors[route['vehicle']]).add_to(map)


    #############CREACION DE MARCADORES PARA RUTAS OPTIMIZADAS#############
    jobs_order = {} #Diccionario para almecenar el orden de los trabajos

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
                arrival_time = step['arrival']
                jobs_order[job_id] = {
                    'order' : order,
                    'vehicle_id' : vehicle_id,
                    'arrival_time' : arrival_time
                }
                order +=1
    
    #Creamos los marcadores para las entregas
    for index, coord in enumerate(dest_coords):
        info = jobs_order.get(index)
        if(info):
            minutos = int(info['arrival_time']//60)
            segundos = int(info['arrival_time']%60)
            popup_text = f"Entrega #{info['order']} (Vehículo: {info['vehicle_id']}) (Tiempo: {minutos}min {segundos}s)"
        else:
            popup_text = "Entrega no asignada"

        folium.Marker(location=list(reversed(coord)),
                     popup=popup_text,
                     icon=folium.Icon(color='blue')).add_to(map)
    #############FIN DE CREACION DE MARCADORES PARA RUTAS OPTIMIZADAS#############


    #Guardado del mapa en un archivo HTML
    map.save('map.html')
