from math import ceil

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import VipTrial, user_has_active_vip


def features(request):
    return render(
        request,
        "features.html",
        {"vip_active": user_has_active_vip(request.user)},
    )


@login_required
def ask_me(request):
    return render(request, "ask_me.html")


@login_required
@require_http_methods(["GET", "POST"])
def vip_membership(request):
    if request.method == "POST":
        trial, created = VipTrial.objects.get_or_create(user=request.user)
        if created:
            messages.success(request, "Your one-month VIP trial has started. No payment method is needed and no automatic charge will occur.")
        else:
            messages.info(request, "Your one-time VIP trial has already been used.")
        return redirect("profiles:vip")

    try:
        trial = request.user.vip_trial
    except VipTrial.DoesNotExist:
        trial = None

    now = timezone.now()
    trial_ends = trial.ends_at if trial else None
    trial_active = trial.is_active(now) if trial else False
    days_remaining = (
        max(0, ceil((trial_ends - now).total_seconds() / 86400))
        if trial_active
        else 0
    )

    return render(
        request,
        "vip/membership.html",
        {
            "trial_started": trial is not None,
            "trial_active": trial_active,
            "trial_ends": trial_ends,
            "days_remaining": days_remaining,
        },
    )
