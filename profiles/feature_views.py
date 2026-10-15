from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def features(request):
    return render(request, "features.html")


@login_required
def ask_me(request):
    return render(request, "ask_me.html")

@login_required
def vip_membership(request):
    from calendar import monthrange
    from django.utils import timezone

    joined = request.user.date_joined
    month = joined.month % 12 + 1
    year = joined.year + (1 if joined.month == 12 else 0)
    day = min(joined.day, monthrange(year, month)[1])
    trial_ends = joined.replace(year=year, month=month, day=day)

    now = timezone.now()
    trial_active = now < trial_ends
    days_remaining = max(0, (trial_ends - now).days)

    return render(
        request,
        "vip/membership.html",
        {
            "trial_active": trial_active,
            "trial_ends": trial_ends,
            "days_remaining": days_remaining,
        },
    )
