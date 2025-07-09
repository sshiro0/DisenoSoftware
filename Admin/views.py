from django.shortcuts import render

# Create your views here.
def create_paquete(request):
    if request.method == 'POST':
        pass
    return render(request, 'Admin_Paquete.html')

def create_Conductor(request):
    if request.method == 'POST':
        pass
    return render(request, 'Admin_CrearConductor.html')