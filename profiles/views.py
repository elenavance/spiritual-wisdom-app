from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from lunar_python import Solar

from .forms import BirthProfileForm
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
