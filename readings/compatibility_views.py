from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from profiles.forms import BirthProfileForm
from profiles.models import BirthProfile
from profiles.services.bazi import (
    CONTROLS,
    GENERATES,
    calculate_birth_reading,
)
from profiles.services.chart_analysis import build_chart_analysis

from lunar_python import Solar

from .elements_compatibility import describe_element_relationship


def _build_person_chart(profile):
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
    eight_char.setSect(2)

    analysis = build_chart_analysis(profile)

    return {
        "profile": profile,
        "reading": reading,
        "analysis": analysis,
        "day_element": reading["day_master"]["element"],
        "eight_char": eight_char,
    }


@login_required
@require_http_methods(["GET", "POST"])
def love_compatibility(request):
    try:
        own_profile = request.user.birth_profile
    except BirthProfile.DoesNotExist:
        own_profile = None

    form = BirthProfileForm(
        request.POST or None,
        instance=BirthProfile(),
    )

    context = {
        "form": form,
        "needs_profile": own_profile is None,
        "compatibility": None,
    }

    if own_profile is None:
        return render(
            request,
            "readings/love_compatibility.html",
            context,
        )

    if request.method == "POST" and form.is_valid():
        partner_profile = form.save(commit=False)

        your_chart = _build_person_chart(own_profile)
        partner_chart = _build_person_chart(partner_profile)

        element_result = describe_element_relationship(
            your_chart["day_element"],
            partner_chart["day_element"],
        )

        context.update({
            "your_chart": your_chart,
            "partner_chart": partner_chart,
            "compatibility": element_result,
        })

    return render(
        request,
        "readings/love_compatibility.html",
        context,
    )
