from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from lunar_python import Solar

from .forms import BirthProfileForm, GuestBaZiForm
from .models import BirthProfile
from .services.bazi import calculate_birth_reading
from .services.elements import analyze_five_elements
from .services.strength import analyze_day_master_strength
from .services.useful_elements import analyze_useful_elements
from .services.interpretation import generate_chart_interpretation


def home(request):
    return render(request, "home.html")


@login_required
def edit_profile(request):
    profile = BirthProfile.objects.filter(user=request.user).first()
    if profile is None:
        profile = BirthProfile(user=request.user)

    form = BirthProfileForm(request.POST or None, instance=profile, language=request.session.get("app_language", "en"))

    if request.method == "POST" and form.is_valid():
        saved_profile = form.save(commit=False)
        saved_profile.user = request.user
        saved_profile.save()
        messages.success(request, "Your birth profile has been saved.")
        return redirect("profiles:edit_profile")

    reading = None
    elements = None
    strength = None
    useful_elements = None
    interpretation = None

    if profile.pk and profile.birth_date:
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
        "profiles/profile_form.html",
        {
            "form": form,
            "profile": profile,
            "reading": reading,
            "elements": elements,
            "strength": strength,
            "useful_elements": useful_elements,
            "interpretation": interpretation,
            "has_hour_pillar": bool(profile.birth_time),
        },
    )


def guest_bazi(request):
    """Allow one anonymous BaZi calculation per browser session."""
    from types import SimpleNamespace
    import json

    from django.views.decorators.http import require_http_methods

    used = request.session.get("guest_bazi_used", False)
    result = request.session.get("guest_bazi_result")
    form = GuestBaZiForm(request.POST or None)

    if request.method == "POST":
        if used:
            messages.info(
                request,
                "Your free guest calculation has already been used in this browser session. Create an account to save and continue with your personal chart.",
            )
            return redirect("profiles:guest_bazi")

        if form.is_valid():
            data = form.cleaned_data
            profile = SimpleNamespace(
                birth_date=data["birth_date"],
                birth_time=data["birth_time"],
                birth_place=data["birth_place"],
                gender=data["gender"],
            )
            reading = calculate_birth_reading(profile)
            birth_time = data["birth_time"]
            solar = Solar.fromYmdHms(
                data["birth_date"].year,
                data["birth_date"].month,
                data["birth_date"].day,
                birth_time.hour if birth_time else 12,
                birth_time.minute if birth_time else 0,
                birth_time.second if birth_time else 0,
            )
            eight_char = solar.getLunar().getEightChar()
            eight_char.setSect(2)
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

            result = {
                "reading": reading,
                "elements": elements,
                "strength": strength,
                "useful_elements": useful_elements,
                "interpretation": interpretation,
            }
            # Normalize to JSON-safe primitives for Django's session serializer.
            result = json.loads(json.dumps(result, ensure_ascii=False))
            request.session["guest_bazi_result"] = result
            request.session["guest_bazi_used"] = True
            request.session.modified = True
            used = True
            messages.success(
                request,
                "Your one free guest chart is ready. Your birth details have not been saved to a member profile.",
            )

    return render(
        request,
        "profiles/guest_bazi.html",
        {
            "form": form if not used else None,
            "result": result,
            "used": used,
        },
    )


def buddhist_wisdom(request):
    """Public educational page with clearly identified Buddhist source texts."""
    return render(request, "buddhist_wisdom.html")
