from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def roles_permitidos(*roles):
    """Restringe una vista a usuarios autenticados que tengan uno de los roles indicados."""
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.rol not in roles:
                raise PermissionDenied("No tienes permiso para acceder a esta sección.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
