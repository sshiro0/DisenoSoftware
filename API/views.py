from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login

User = get_user_model()


def login_user(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type', 'Login')

        if form_type == 'Register':
            try:
                CustomUser.objects.create_user(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    tipo_usuario='CL',
                    direccion=request.POST.get('direccion', '')
                )
                messages.success(request, 'Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
            except Exception as e:
                messages.error(request, f'Error al registrar: {str(e)}')

        else:  # form_type == 'Login'
            correo = request.POST['correo']
            contrasena = request.POST['contrasena']

            try:
                usuario = CustomUser.objects.get(email=correo)
            except CustomUser.DoesNotExist:
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
                    return redirect('admin_login')
                else:
                    messages.error(request, 'Tu cuenta no tiene un tipo de usuario válido.')
            else:
                messages.error(request, 'Correo o contraseña incorrectos.')

    return render(request, 'login.html')
