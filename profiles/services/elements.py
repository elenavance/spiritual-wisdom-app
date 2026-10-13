
from collections import Counter

from .bazi import STEM_ELEMENT, ELEMENT_EN


BRANCH_ELEMENT = {
    "子": "Water",
    "丑": "Earth",
    "寅": "Wood",
    "卯": "Wood",
    "辰": "Earth",
    "巳": "Fire",
    "午": "Fire",
    "未": "Earth",
    "申": "Metal",
    "酉": "Metal",
    "戌": "Earth",
    "亥": "Water",
}

ELEMENT_ORDER = ("Wood", "Fire", "Earth", "Metal", "Water")


def analyze_five_elements(eight_char, include_hour=True):
    """
    Summarize the structural occurrence of the five elements.

    Counts visible stems, branch elements, and hidden stems separately.
    These counts describe chart composition; they do not determine
    Day Master strength, favorable elements, or useful gods.
    """
    pillars = [
        (
            "Year",
            eight_char.getYearGan(),
            eight_char.getYearZhi(),
            eight_char.getYearHideGan(),
        ),
        (
            "Month",
            eight_char.getMonthGan(),
            eight_char.getMonthZhi(),
            eight_char.getMonthHideGan(),
        ),
        (
            "Day",
            eight_char.getDayGan(),
            eight_char.getDayZhi(),
            eight_char.getDayHideGan(),
        ),
    ]

    if include_hour:
        pillars.append(
            (
                "Hour",
                eight_char.getTimeGan(),
                eight_char.getTimeZhi(),
                eight_char.getTimeHideGan(),
            )
        )

    visible_counts = Counter()
    branch_counts = Counter()
    hidden_counts = Counter()
    details = []

    for name, stem, branch, hidden_stems in pillars:
        stem_element = STEM_ELEMENT.get(stem)
        branch_element = BRANCH_ELEMENT.get(branch)

        hidden_stems = list(hidden_stems or [])
        hidden_details = []

        if stem_element:
            visible_counts[stem_element] += 1

        if branch_element:
            branch_counts[branch_element] += 1

        for hidden_stem in hidden_stems:
            hidden_element = STEM_ELEMENT.get(hidden_stem)

            if not hidden_element:
                continue

            hidden_counts[hidden_element] += 1
            hidden_details.append({
                "stem": hidden_stem,
                "element": hidden_element,
                "element_english": ELEMENT_EN.get(
                    hidden_element, hidden_element
                ),
            })

        details.append({
            "pillar": name,
            "stem": stem,
            "stem_element": stem_element,
            "stem_element_english": ELEMENT_EN.get(
                stem_element, stem_element
            ),
            "branch": branch,
            "branch_element": branch_element,
            "branch_element_english": ELEMENT_EN.get(
                branch_element, branch_element
            ),
            "hidden_stems": hidden_stems,
            "hidden_elements": [
                item["element"] for item in hidden_details
            ],
            "hidden_details": hidden_details,
        })

    structural_totals = {
        element: (
            visible_counts[element]
            + branch_counts[element]
            + hidden_counts[element]
        )
        for element in ELEMENT_ORDER
    }

    total_occurrences = sum(structural_totals.values())

    structural_percentages = {
        element: (
            round(
                structural_totals[element] / total_occurrences * 100,
                1,
            )
            if total_occurrences
            else 0
        )
        for element in ELEMENT_ORDER
    }

    return {
        "method": (
            "Structural occurrence count: each visible stem, branch "
            "element, and hidden stem is counted separately. A branch "
            "element is a simplified representation of the branch, "
            "not a substitute for its hidden stems. These totals and "
            "percentages are descriptive only; they do not establish "
            "Day Master strength or favorable elements."
        ),
        "elements": list(ELEMENT_ORDER),
        "visible_stem_counts": {
            element: visible_counts[element]
            for element in ELEMENT_ORDER
        },
        "branch_element_counts": {
            element: branch_counts[element]
            for element in ELEMENT_ORDER
        },
        "hidden_stem_counts": {
            element: hidden_counts[element]
            for element in ELEMENT_ORDER
        },
        "structural_totals": structural_totals,
        "structural_percentages": structural_percentages,
        "total_occurrences": total_occurrences,
        "has_hour_pillar": include_hour,
        "pillars": details,
    }
