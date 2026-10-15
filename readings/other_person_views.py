from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from lunar_python import Solar

from profiles.forms import BirthProfileForm
from profiles.models import BirthProfile
from profiles.services.bazi import calculate_birth_reading
from profiles.services.elements import analyze_five_elements
from profiles.services.chart_analysis import build_chart_analysis


@login_required
def test_another_person(request):
    form = BirthProfileForm(
        request.POST or None,
        instance=BirthProfile(),
    )

    context = {"form": form, "reading": None}

    if request.method == "POST" and form.is_valid():
        profile = form.save(commit=False)

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
            eight_char,
            include_hour=include_hour,
        )
        analysis = build_chart_analysis(profile)

        context.update({
            "profile": profile,
            "reading": reading,
            "elements": elements,
            "strength": analysis["strength"],
            "useful_elements": analysis["useful_elements"],
            "interpretation": analysis["interpretation"],
        })

    return render(
        request,
        "readings/other_person.html",
        context,
    )
