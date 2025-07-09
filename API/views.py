from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout

User = get_user_model()


def login_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')

    if request.method == 'POST':
        correo = request.POST['correo']
        contrasena = request.POST['contrasena']

        # Autenticación usando email como identificador
        try:
            usuario = User.objects.get(email=correo)
        except User.DoesNotExist:
            messages.error(request, 'Correo o contraseña incorrectos.')
            return render(request, 'login.html')
            

        user = authenticate(request, username=usuario.username, password=contrasena)

        if user is not None:
            login(request, user)
            tipo = user.tipo_usuario.strip().upper()

            if tipo == 'CL':
                return redirect('ver_paquetes_cliente', id=user.id)

            elif tipo == 'CO':
                return redirect('ver_entregas')

            elif tipo == 'AD':
                return redirect('admin_login')  # o tu vista: redirect('panel_admin')

            else:
                messages.error(request, 'Tu cuenta no tiene un tipo de usuario válido.')
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')

    return render(request, 'login.html')