from django.http import HttpResponseForbidden

class RoleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func, 'view_class'):  # Para vistas basadas en clase
            view_class = view_func.view_class
            if hasattr(view_class, 'decorators'):
                for decorator in view_class.decorators:
                    if decorator.__name__ == 'admin_required' and request.user.tipo_usuario != 'Ad':
                        return HttpResponseForbidden()
                    # Añadir checks similares para otros roles