from django.http import HttpResponseForbidden
from functools import wraps

def family_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.family:
            return HttpResponseForbidden("You are not part of a family.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view