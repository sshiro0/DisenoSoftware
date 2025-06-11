from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, "Debes iniciar sesión")
                return redirect('login')
                
            if request.user.tipo_usuario != role:
                messages.error(request, "No tienes permisos para esta sección")
                return redirect('dashboard')
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

admin_required = role_required('Ad')
conductor_required = role_required('Co')
cliente_required = role_required('Cl')