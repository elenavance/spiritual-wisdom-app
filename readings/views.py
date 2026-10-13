from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from lunar_python import Solar

from profiles.models import BirthProfile
from profiles.services.bazi import calculate_birth_reading
from profiles.services.elements import analyze_five_elements


@login_required
def dashboard(request):
    profile = BirthProfile.objects.filter(user=request.user).first()

    if profile is None or not profile.birth_date:
        return redirect("profiles:edit")

    reading = calculate_birth_reading(profile)

    birth_time = profile.birth_time
    solar = Solar.fromYmdHms(
        profile.birth_date.year,
        profile.birth_date.month,
        profile.birth_date.day,
        birth_time.hour if birth_time else 12,
        birth_time.minute if birth_time else 0,
        birth_time.second if birth_time else 0,
    )

    elements = analyze_five_elements(
        solar.getLunar().getEightChar(),
        include_hour=bool(birth_time),
    )

    return render(
        request,
        "readings/dashboard.html",
        {
            "profile": profile,
            "reading": reading,
            "elements": elements,
        },
    )
