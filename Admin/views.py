from django.shortcuts import render

# Create your views here.
def create_paquete(request):
    if request.method == 'POST':
        pass
    return render(request, 'Admin_Paquete.html')
def create_paquete(request):
    if request.method == 'POST':
        data = {
            'remitente': request.POST['remitente'],
            'direccion': request.POST['direccion'],
            'origen': request.POST['origen'],
            'peso': request.POST['peso'],
            'dimensiones': request.POST['dimensiones'],
            'instrucciones': request.POST['instrucciones'],
            'contenido': request.POST['contenido'],
            'estado': request.POST['estado'],
        }   

    return render(request, 'Admin_Paquete.html')

def Admin(request):
    if request.method == 'POST':
        pass
    return render(request, 'Admin.html')