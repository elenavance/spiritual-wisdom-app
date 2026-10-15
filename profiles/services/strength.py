
"""Explainable, preliminary BaZi Day Master strength analysis.

This is a transparent heuristic, not a universally accepted classical
strength formula. It reports the contributing factors separately.
"""

from profiles.services.bazi import STEM_ELEMENT
from profiles.services.elements import ELEMENT_ORDER


GENERATES = {
    "Wood": "Fire",
    "Fire": "Earth",
    "Earth": "Metal",
    "Metal": "Water",
    "Water": "Wood",
}

CONTROLS = {
    "Wood": "Earth",
    "Earth": "Water",
    "Water": "Fire",
    "Fire": "Metal",
    "Metal": "Wood",
}


def _element_from_stem(stem):
    return STEM_ELEMENT.get(stem)


def analyze_day_master_strength(eight_char, include_hour=True):
    """Return transparent factors and a preliminary strength assessment."""
    day_stem = eight_char.getDayGan()
    day_element = _element_from_stem(day_stem)

    if not day_element:
        raise ValueError("Unable to determine the Day Master element.")

    pillars = [
        ("Year", eight_char.getYearGan(), eight_char.getYearZhi(),
         eight_char.getYearHideGan()),
        ("Month", eight_char.getMonthGan(), eight_char.getMonthZhi(),
         eight_char.getMonthHideGan()),
        ("Day", eight_char.getDayGan(), eight_char.getDayZhi(),
         eight_char.getDayHideGan()),
    ]

    if include_hour:
        pillars.append((
            "Hour",
            eight_char.getTimeGan(),
            eight_char.getTimeZhi(),
            eight_char.getTimeHideGan(),
        ))

    resource_element = next(
        element for element in ELEMENT_ORDER
        if GENERATES[element] == day_element
    )
    output_element = GENERATES[day_element]
    wealth_element = CONTROLS[day_element]
    officer_element = next(
        element for element in ELEMENT_ORDER
        if CONTROLS[element] == day_element
    )

    # Transparent structural weights: visible stems count once;
    # hidden stems count fractionally; the Month Branch gets extra weight.
    support = 0.0
    pressure = 0.0
    details = []
    root_count = 0

    for name, stem, branch, hidden_stems in pillars:
        stem_element = _element_from_stem(stem)
        hidden_stems = list(hidden_stems or [])
        is_month = name == "Month"

        stem_weight = 1.0
        branch_weight = 2.0 if is_month else 1.0
        hidden_weight = 0.5

        if stem_element in (day_element, resource_element):
            contribution = stem_weight * (1.25 if is_month else 1.0)
            support += contribution
        else:
            contribution = 0.0

        hidden_support = 0.0
        hidden_pressure = 0.0

        for hidden in hidden_stems:
            element = _element_from_stem(hidden)
            if element in (day_element, resource_element):
                hidden_support += hidden_weight
                if element == day_element:
                    root_count += 1
            elif element in (wealth_element, officer_element, output_element):
                hidden_pressure += hidden_weight

        support += hidden_support * branch_weight
        pressure += hidden_pressure * branch_weight

        # The Month Branch is a coarse seasonal proxy. It is not a
        # full solar-term strength calculation.
        branch_element = {
            "子": "Water", "丑": "Earth", "寅": "Wood",
            "卯": "Wood", "辰": "Earth", "巳": "Fire",
            "午": "Fire", "未": "Earth", "申": "Metal",
            "酉": "Metal", "戌": "Earth", "亥": "Water",
        }.get(branch)

        seasonal_support = 0.0
        if is_month and branch_element in (day_element, resource_element):
            seasonal_support = 2.0
            support += seasonal_support

        details.append({
            "pillar": name,
            "stem": stem,
            "stem_element": stem_element,
            "branch": branch,
            "branch_element": branch_element,
            "hidden_stems": hidden_stems,
            "support_contribution": round(
                contribution + hidden_support * branch_weight
                + seasonal_support, 2
            ),
            "pressure_contribution": round(
                hidden_pressure * branch_weight, 2
            ),
        })

    total = support + pressure
    ratio = support / total if total else 0.5

    if ratio >= 0.65:
        category = "strong"
        label = "Preliminarily strong"
    elif ratio <= 0.40:
        category = "weak"
        label = "Preliminarily weak"
    else:
        category = "balanced"
        label = "Intermediate support balance"

    return {
        "day_master_stem": day_stem,
        "day_master_element": day_element,
        "resource_element": resource_element,
        "output_element": output_element,
        "wealth_element": wealth_element,
        "officer_element": officer_element,
        "support_score": round(support, 2),
        "pressure_score": round(pressure, 2),
        "support_ratio": round(ratio, 3),
        "root_count": root_count,
        "category": category,
        "label": label,
        "method": (
            "Preliminary structural heuristic. Visible stems count once, "
            "hidden stems fractionally, and the Month Branch receives extra "
            "weight. This does not fully model solar-term seasonal strength, "
            "stem combinations, transformations, or all classical schools. "
            "It must not be treated as a definitive traditional verdict."
        ),
        "pillars": details,
    }
