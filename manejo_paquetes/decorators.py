from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps

#def admin_required(view_func):
#    @wraps(view_func)
#    def _wrapped_view(request, *args, **kwargs):
#        if not request.user.tipo_usuario == 'Ad' or request.user.estado != 'A':
#            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
#        return view_func(request, *args, **kwargs)
#    return _wrapped_view

#def conductor_required(view_func):
#    @wraps(view_func)
#    def _wrapped_view(request, *args, **kwargs):
#        if not request.user.tipo_usuario == 'Co' or request.user.estado != 'A':
#            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
#        return view_func(request, *args, **kwargs)
#    return _wrapped_view

#def cliente_required(view_func):
#    @wraps(view_func)
#    def _wrapped_view(request, *args, **kwargs):
#        if not request.user.tipo_usuario == 'Cl' or request.user.estado != 'A':
#            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
#        return view_func(request, *args, **kwargs)
#    return _wrapped_view