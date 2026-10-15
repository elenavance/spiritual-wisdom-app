from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from profiles.services.chart_analysis import build_chart_analysis


ELEMENT_COLORS = {
    "Wood": {
        "name": "Green",
        "hex": "#376B4B",
        "meaning": "Growth, renewal, and flexibility",
    },
    "Fire": {
        "name": "Red",
        "hex": "#A53F32",
        "meaning": "Warmth, energy, and expression",
    },
    "Earth": {
        "name": "Gold",
        "hex": "#A58A45",
        "meaning": "Grounding, stability, and care",
    },
    "Metal": {
        "name": "White",
        "hex": "#E8E3D8",
        "meaning": "Clarity, structure, and refinement",
    },
    "Water": {
        "name": "Blue",
        "hex": "#315B83",
        "meaning": "Reflection, adaptability, and calm",
    },
}


def _reflection_number(birth_date):
    """Return a stable app-defined number from the saved birth date."""
    digits = birth_date.strftime("%Y%m%d")
    total = sum(int(digit) for digit in digits)
    number = total % 9
    return number if number else 9


@login_required
def lucky_color_number(request):
    try:
        profile = request.user.birth_profile
    except Exception:
        profile = None

    context = {
        "profile": profile,
        "colors": [],
        "lucky_number": None,
        "analysis": None,
    }

    if profile and profile.birth_date:
        analysis = build_chart_analysis(profile)
        useful = analysis["useful_elements"]

        candidates = useful.get("primary_candidates", [])
        if not candidates:
            candidates = [analysis["strength"]["day_master_element"]]

        colors = []
        for element in candidates:
            color = ELEMENT_COLORS.get(element)
            if color and color not in colors:
                colors.append({
                    **color,
                    "element": element,
                })

        context.update({
            "lucky_number": _reflection_number(profile.birth_date),
            "colors": colors,
            "analysis": analysis,
            "useful_elements": useful,
        })

    return render(
        request,
        "readings/lucky_color_number.html",
        context,
    )
