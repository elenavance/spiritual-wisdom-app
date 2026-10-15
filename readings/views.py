from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from lunar_python import Solar

from profiles.models import BirthProfile
from profiles.services.bazi import calculate_birth_reading
from profiles.services.elements import analyze_five_elements
from profiles.services.strength import analyze_day_master_strength
from profiles.services.useful_elements import analyze_useful_elements
from profiles.services.interpretation import generate_chart_interpretation


@login_required
def dashboard(request):
    profile = BirthProfile.objects.filter(user=request.user).first()

    if profile is None or not profile.birth_date:
        return redirect("profiles:edit_profile")

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
    eight_char = solar.getLunar().getEightChar()
    include_hour = bool(birth_time)

    elements = analyze_five_elements(
        eight_char, include_hour=include_hour
    )
    strength = analyze_day_master_strength(
        eight_char, include_hour=include_hour
    )
    useful_elements = analyze_useful_elements(strength)
    interpretation = generate_chart_interpretation(
        strength, useful_elements
    )

    return render(
        request,
        "readings/dashboard.html",
        {
            "profile": profile,
            "reading": reading,
            "elements": elements,
            "strength": strength,
            "useful_elements": useful_elements,
            "interpretation": interpretation,
            "has_hour_pillar": bool(profile.birth_time),
        },
    )
