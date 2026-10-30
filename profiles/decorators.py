from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import user_has_active_vip


def vip_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not user_has_active_vip(request.user):
            messages.info(
                request,
                "Start your free one-month VIP trial to use this feature.",
            )
            return redirect("profiles:vip")
        return view_func(request, *args, **kwargs)

    return wrapped
