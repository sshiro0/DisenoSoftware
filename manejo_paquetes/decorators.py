from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.tipo_usuario == 'Ad':
            return redirect('admin')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def conductor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.tipo_usuario == 'Co':
            return redirect('conductor')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def cliente_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.tipo_usuario == 'Cl':
            return redirect('cliente')
        return view_func(request, *args, **kwargs)
    return _wrapped_view