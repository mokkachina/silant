



class RoleCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            return None

        # Проверка доступа к админке
        if request.path.startswith('/admin/') and not request.user.is_manager:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied