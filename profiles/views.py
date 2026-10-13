from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import BirthProfileForm
from .models import BirthProfile
from .services.bazi import calculate_birth_reading
from .services.elements import analyze_five_elements
from lunar_python import Solar


def home(request):
    return render(request, "home.html")


@login_required
def edit_profile(request):
    profile = BirthProfile.objects.filter(user=request.user).first()
    if profile is None:
        profile = BirthProfile(user=request.user)

    form = BirthProfileForm(request.POST or None, instance=profile)

    if request.method == "POST" and form.is_valid():
        saved_profile = form.save(commit=False)
        saved_profile.user = request.user
        saved_profile.save()
        messages.success(request, "Your birth profile has been saved.")
        return redirect("profiles:edit")

    reading = None
    elements = None

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
        elements = analyze_five_elements(
            solar.getLunar().getEightChar(),
            include_hour=bool(birth_time),
        )

    return render(
        request,
        "profiles/profile_form.html",
        {
            "form": form,
            "profile": profile,
            "reading": reading,
            "elements": elements,
        },
    )
