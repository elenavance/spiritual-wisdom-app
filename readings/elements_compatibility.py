def describe_element_relationship(your_element, partner_element):
    """Describe the Day Master element relationship without inventing a score."""
    if not your_element or not partner_element:
        return {
            "title": "A reflective comparison",
            "description": (
                "The element relationship could not be determined from "
                "the available chart data."
            ),
            "reflection": (
                "Consider how you communicate, respond to differences, "
                "and support one another."
            ),
        }

    if your_element == partner_element:
        return {
            "title": "A shared elemental theme",
            "description": (
                f"Both Day Masters are associated with {your_element}. "
                "In traditional Five Elements symbolism, a shared element "
                "can represent familiar approaches or similar priorities. "
                "It may also highlight habits that both people share."
            ),
            "reflection": (
                "Where do your similarities help you understand each other, "
                "and where might you need different perspectives?"
            ),
        }

    from profiles.services.bazi import CONTROLS, GENERATES

    if GENERATES.get(your_element) == partner_element:
        return {
            "title": "A theme of giving and support",
            "description": (
                f"In Five Elements symbolism, {your_element} generates "
                f"{partner_element}. This can be used as a reflection on "
                "support, encouragement, and the balance between giving "
                "and receiving."
            ),
            "reflection": (
                "How can you support each other while making sure both "
                "people's needs are heard?"
            ),
        }

    if GENERATES.get(partner_element) == your_element:
        return {
            "title": "A theme of receiving and renewal",
            "description": (
                f"In Five Elements symbolism, {partner_element} generates "
                f"{your_element}. This can prompt reflection on how care, "
                "encouragement, and shared effort move between two people."
            ),
            "reflection": (
                "How do you each show care, and do you both feel appreciated?"
            ),
        }

    if CONTROLS.get(your_element) == partner_element:
        return {
            "title": "A theme of balance and boundaries",
            "description": (
                f"In Five Elements symbolism, {your_element} controls "
                f"{partner_element}. This is a prompt to consider how "
                "different preferences, boundaries, and decision-making "
                "styles can be balanced respectfully."
            ),
            "reflection": (
                "How can you discuss disagreements without trying to "
                "control each other's choices?"
            ),
        }

    if CONTROLS.get(partner_element) == your_element:
        return {
            "title": "A theme of adjustment and understanding",
            "description": (
                f"In Five Elements symbolism, {partner_element} controls "
                f"{your_element}. This can prompt reflection on adapting "
                "to different needs while maintaining mutual respect."
            ),
            "reflection": (
                "How can you make room for each other's needs and boundaries?"
            ),
        }

    return {
        "title": "A theme for mutual understanding",
        "description": (
            "Use this comparison as a starting point for discussing "
            "different approaches and shared priorities."
        ),
        "reflection": (
            "What helps both of you feel understood and respected?"
        ),
    }
