from functools import wraps
from django.shortcuts import redirect
def permission_required_custom(perm, redirect_to='home'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.has_perm(perm):
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator