from datetime import date, time

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from lunar_python import Solar

from profiles.forms import BirthProfileForm
from profiles.models import BirthProfile
from profiles.services.bazi import calculate_birth_reading
from profiles.services.elements import analyze_five_elements
from profiles.services.strength import analyze_day_master_strength
from profiles.services.useful_elements import analyze_useful_elements
from profiles.services.interpretation import generate_chart_interpretation


GUEST_PROFILE_SESSION_KEY = "guest_reading_profile"


@require_http_methods(["GET", "POST"])
def preview(request):
    form = BirthProfileForm(
        request.POST or None,
        language=request.session.get("app_language", "en"),
    )
    if request.method == "POST" and form.is_valid():
        profile = form.save(commit=False)
        request.session[GUEST_PROFILE_SESSION_KEY] = {
            "display_name": profile.display_name,
            "gender": profile.gender,
            "birth_date": profile.birth_date.isoformat(),
            "birth_time": profile.birth_time.isoformat() if profile.birth_time else "",
            "birth_place": profile.birth_place,
            "birth_timezone": profile.birth_timezone,
        }
        request.session.set_expiry(3600)
        return redirect("readings:dashboard")
    return render(request, "readings/preview.html", {"form": form})


def dashboard(request):
    is_guest = not request.user.is_authenticated
    if is_guest:
        payload = request.session.get(GUEST_PROFILE_SESSION_KEY)
        if not isinstance(payload, dict):
            return redirect("readings:preview")
        try:
            profile = BirthProfile(
                display_name=payload.get("display_name", ""),
                gender=payload.get("gender", ""),
                birth_date=date.fromisoformat(payload["birth_date"]),
                birth_time=time.fromisoformat(payload["birth_time"]) if payload.get("birth_time") else None,
                birth_place=payload.get("birth_place", ""),
                birth_timezone=payload.get("birth_timezone", ""),
            )
        except (KeyError, TypeError, ValueError):
            request.session.pop(GUEST_PROFILE_SESSION_KEY, None)
            messages.info(request, "Please enter your birth details to prepare a reading.")
            return redirect("readings:preview")
    else:
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
    elements = analyze_five_elements(eight_char, include_hour=include_hour)
    strength = analyze_day_master_strength(eight_char, include_hour=include_hour)
    useful_elements = analyze_useful_elements(strength)
    interpretation = generate_chart_interpretation(strength, useful_elements)

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
            "is_guest_reading": is_guest,
        },
    )
