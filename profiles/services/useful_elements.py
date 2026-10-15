
"""Preliminary useful-element analysis built on Day Master strength."""

from profiles.services.bazi import STEM_ELEMENT
from profiles.services.strength import GENERATES, CONTROLS


def analyze_useful_elements(strength):
    """Suggest provisional elements based on the strength heuristic.

    These are educational suggestions, not a definitive classical
    determination of Yong Shen or Xi Shen.
    """
    day_element = strength["day_master_element"]

    resource_element = next(
        element for element in GENERATES
        if GENERATES[element] == day_element
    )
    output_element = GENERATES[day_element]
    wealth_element = CONTROLS[day_element]
    officer_element = next(
        element for element in CONTROLS
        if CONTROLS[element] == day_element
    )

    category = strength["category"]

    if category == "weak":
        primary = [day_element, resource_element]
        secondary = [output_element, wealth_element, officer_element]
        explanation = (
            "The preliminary chart heuristic indicates less structural "
            "support for the Day Master. Its own element and its resource "
            "element are listed as candidates for further review."
        )
    elif category == "strong":
        primary = [output_element, wealth_element, officer_element]
        secondary = [day_element, resource_element]
        explanation = (
            "The preliminary chart heuristic indicates substantial "
            "structural support. Output, wealth, and officer elements are "
            "listed as candidates for further review."
        )
    else:
        primary = [output_element, resource_element]
        secondary = [day_element, wealth_element, officer_element]
        explanation = (
            "The preliminary support balance is intermediate. No single "
            "element can be confidently selected from this heuristic alone."
        )

    return {
        "method": "Preliminary candidates derived from the strength heuristic",
        "status": "provisional",
        "primary_candidates": primary,
        "secondary_candidates": secondary,
        "not_a_definitive_yong_shen": True,
        "explanation": explanation,
        "limitations": (
            "A full traditional useful-element assessment may require "
            "solar-term seasonal strength, chart structure, combinations, "
            "climate considerations, and school-specific rules. Element "
            "counts alone cannot establish a definitive favorable element."
        ),
    }
