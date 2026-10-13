from collections import Counter

from .bazi import STEM_ELEMENT, ELEMENT_EN


BRANCH_ELEMENT = {
    "子": "Water", "丑": "Earth", "寅": "Wood", "卯": "Wood",
    "辰": "Earth", "巳": "Fire", "午": "Fire", "未": "Earth",
    "申": "Metal", "酉": "Metal", "戌": "Earth", "亥": "Water",
}


def analyze_five_elements(eight_char, include_hour=True):
    """
    Return transparent element counts for a lunar_python EightChar object.

    Each visible stem, branch, and hidden stem is counted as one occurrence.
    These are structural counts, not traditional BaZi strength calculations.
    """
    pillars = [
        ("Year", eight_char.getYearGan(), eight_char.getYearZhi(),
         eight_char.getYearHideGan()),
        ("Month", eight_char.getMonthGan(), eight_char.getMonthZhi(),
         eight_char.getMonthHideGan()),
        ("Day", eight_char.getDayGan(), eight_char.getDayZhi(),
         eight_char.getDayHideGan()),
    ]

    if include_hour:
        pillars.append(
            ("Hour", eight_char.getTimeGan(), eight_char.getTimeZhi(),
             eight_char.getTimeHideGan())
        )

    visible_counts = Counter()
    hidden_counts = Counter()
    branch_counts = Counter()
    details = []

    for name, stem, branch, hidden_stems in pillars:
        stem_element = STEM_ELEMENT.get(stem)
        branch_element = BRANCH_ELEMENT.get(branch)
        hidden_elements = [
            STEM_ELEMENT[hidden] for hidden in hidden_stems
            if hidden in STEM_ELEMENT
        ]

        if stem_element:
            visible_counts[stem_element] += 1
        if branch_element:
            branch_counts[branch_element] += 1
        hidden_counts.update(hidden_elements)

        details.append({
            "pillar": name,
            "stem": stem,
            "stem_element": stem_element,
            "branch": branch,
            "branch_element": branch_element,
            "hidden_stems": list(hidden_stems),
            "hidden_elements": hidden_elements,
        })

    all_elements = ("Wood", "Fire", "Earth", "Metal", "Water")
    totals = {
        element: (
            visible_counts[element]
            + branch_counts[element]
            + hidden_counts[element]
        )
        for element in all_elements
    }

    return {
        "method": (
            "Structural occurrence count: visible stems, branch elements, "
            "and hidden stems each count once. This is not a BaZi strength "
            "or favorable-element calculation."
        ),
        "visible_stem_counts": {
            element: visible_counts[element] for element in all_elements
        },
        "branch_element_counts": {
            element: branch_counts[element] for element in all_elements
        },
        "hidden_stem_counts": {
            element: hidden_counts[element] for element in all_elements
        },
        "structural_totals": totals,
        "pillars": details,
    }
