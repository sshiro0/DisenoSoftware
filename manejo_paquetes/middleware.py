from django.http import HttpResponseForbidden

class RoleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func, 'admin_required') and not request.user.tipo_usuario == 'Ad':
            return HttpResponseForbidden()
        if hasattr(view_func, 'conductor_required') and not request.user.tipo_usuario == 'Co':
            return HttpResponseForbidden()
        if hasattr(view_func, 'cliente_required') and not request.user.tipo_usuario == 'Cl':
            return HttpResponseForbidden()
        return None