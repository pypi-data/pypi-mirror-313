from functools import wraps
from django.http import HttpResponseForbidden
from .permissions import check_user_role

def role_required(role):
    """Decorator to restrict view access to a specific role."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not check_user_role(request.user, role):
                return HttpResponseForbidden("You don't have permission to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
