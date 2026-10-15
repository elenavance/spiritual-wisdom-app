"""Shared integration for educational BaZi chart analysis."""

from lunar_python import Solar

from profiles.services.interpretation import generate_chart_interpretation
from profiles.services.strength import analyze_day_master_strength
from profiles.services.useful_elements import analyze_useful_elements


def build_chart_analysis(profile):
    """Build strength, useful-element, and interpretation data for a profile."""
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

    include_hour = bool(birth_time)
    strength = analyze_day_master_strength(
        eight_char,
        include_hour=include_hour,
    )
    useful_elements = analyze_useful_elements(strength)
    interpretation = generate_chart_interpretation(
        strength,
        useful_elements,
    )

    return {
        "strength": strength,
        "useful_elements": useful_elements,
        "interpretation": interpretation,
        "has_hour_pillar": include_hour,
    }
