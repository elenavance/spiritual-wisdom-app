"""Educational BaZi interpretations for cultural learning and reflection."""

ELEMENT_THEMES = {
    "Wood": {
        "personality": "Wood symbolizes growth, learning, planning, and a forward-looking approach. Reflect on how you set goals and respond when plans change.",
        "career": "Wood symbolism is linked with development, education, planning, and helping ideas grow. Consider where you can learn, organize, or build something useful.",
        "relationships": "Wood symbolism emphasizes shared growth, patience, and room for each person to develop. Healthy relationships also need listening and mutual respect.",
        "development": "Reflect on your goals, adaptability, and the balance between persistence and flexibility.",
        "money": "Wood can symbolize gradual growth and long-term planning. Review whether your financial goals are realistic and supported by consistent habits.",
        "family": "Wood symbolism invites reflection on how family members can grow while respecting different needs, boundaries, and viewpoints.",
        "wellbeing": "Use this theme as a reminder to create sustainable routines and make room for rest. A BaZi chart cannot assess your medical condition.",
    },
    "Fire": {
        "personality": "Fire symbolizes warmth, enthusiasm, expression, and visibility. Reflect on how you share ideas and balance activity with quiet time.",
        "career": "Fire symbolism is linked with communication, presentation, creativity, and public engagement. Consider how these activities fit your actual skills and interests.",
        "relationships": "Fire symbolism emphasizes warmth, openness, appreciation, and clear expression of feelings. Listening is as important as expressing yourself.",
        "development": "Balance enthusiasm with rest, listening, and considered decisions.",
        "money": "Fire can symbolize energy and visibility. Before spending, consider whether a purchase supports your priorities or meets a temporary impulse.",
        "family": "Fire symbolism invites reflection on appreciation, open conversation, and making space for quieter family members to speak.",
        "wellbeing": "Consider whether your daily schedule leaves room for rest and recovery. Traditional symbolism cannot diagnose illness or predict health outcomes.",
    },
    "Earth": {
        "personality": "Earth symbolizes stability, reliability, practicality, and care. Reflect on how you create security while remaining open to new information.",
        "career": "Earth symbolism is linked with organization, operations, administration, and long-term responsibilities. Consider where steady, practical work serves you well.",
        "relationships": "Earth symbolism emphasizes dependability, consistency, and practical expressions of care. Remember that support also includes honest conversation.",
        "development": "Build stability while remaining open to new information and necessary change.",
        "money": "Earth can symbolize stability and careful planning. Review your budget, emergency savings, and long-term commitments using your real financial circumstances.",
        "family": "Earth symbolism invites reflection on shared responsibilities and dependable support, without assuming one person must carry every burden.",
        "wellbeing": "Reflect on whether your routines support rest, movement, and emotional wellbeing. Seek qualified care for health concerns.",
    },
    "Metal": {
        "personality": "Metal symbolizes structure, discernment, precision, standards, and refinement. Reflect on how your standards help you and when flexibility may be useful.",
        "career": "Metal symbolism is linked with quality control, analysis, systems, and careful decisions. Consider where accuracy and clear processes are genuine strengths.",
        "relationships": "Metal symbolism emphasizes honesty, boundaries, reliability, and clear expectations. Try to combine directness with kindness and curiosity.",
        "development": "Maintain high standards without becoming overly rigid or self-critical.",
        "money": "Metal can symbolize structure and discernment. Clear records and deliberate decisions may help you manage money according to your circumstances.",
        "family": "Metal symbolism invites reflection on fair boundaries, clear expectations, and respectful disagreement within family relationships.",
        "wellbeing": "Consider whether high standards create unnecessary pressure. This reflection is not a medical assessment or a substitute for professional advice.",
    },
    "Water": {
        "personality": "Water symbolizes reflection, adaptability, observation, and the movement of information. Reflect on how you use curiosity while maintaining direction.",
        "career": "Water symbolism is linked with research, strategy, communication, negotiation, and responding to change. Consider how these themes relate to your experience.",
        "relationships": "Water symbolism emphasizes listening, emotional awareness, adaptability, and thoughtful communication. Clear boundaries matter alongside understanding.",
        "development": "Use observation and flexibility while maintaining clear direction and boundaries.",
        "money": "Water can symbolize flexibility and information. Gather reliable facts and consider risks rather than relying on symbolic guidance for financial decisions.",
        "family": "Water symbolism invites reflection on listening carefully, discussing concerns calmly, and adapting communication to different family needs.",
        "wellbeing": "Make space for reflection and supportive routines. A traditional chart cannot diagnose health conditions or determine your wellbeing.",
    },
}

STRENGTH_NOTES = {
    "strong": (
        "This preliminary heuristic identifies substantial structural support "
        "for the Day Master. It is not a fixed personality judgment or a guarantee."
    ),
    "weak": (
        "This preliminary heuristic identifies less structural support for "
        "the Day Master. It does not mean personal weakness or predict poor outcomes."
    ),
    "balanced": (
        "This preliminary heuristic finds an intermediate support balance. "
        "It does not establish that every area of life is balanced."
    ),
}


def generate_chart_interpretation(strength, useful_elements):
    """Return compatible chart sections and expanded life-reflection sections."""
    element = strength.get("day_master_element")
    category = strength.get("category")

    if element not in ELEMENT_THEMES:
        raise ValueError("A valid Day Master element is required.")
    if category not in STRENGTH_NOTES:
        raise ValueError("A valid preliminary strength category is required.")

    themes = ELEMENT_THEMES[element]
    candidates = useful_elements.get("primary_candidates", [])
    candidate_text = ", ".join(candidates) if candidates else (
        "No primary element candidates were selected."
    )

    life_sections = [
        {
            "key": "personality",
            "title": "Personality and Natural Tendencies",
            "summary": themes["personality"],
            "reflection": "Which parts of this traditional symbolism match your lived experience, and which do not?",
        },
        {
            "key": "career",
            "title": "Career and Working Style",
            "summary": themes["career"],
            "reflection": "Which tasks use your skills well, based on your actual experience and interests?",
        },
        {
            "key": "relationships",
            "title": "Love and Relationships",
            "summary": themes["relationships"],
            "reflection": "What need or expectation could you communicate more clearly in an important relationship?",
        },
        {
            "key": "money",
            "title": "Money and Financial Habits",
            "summary": themes["money"],
            "reflection": "What realistic step could you take toward greater financial clarity or stability?",
        },
        {
            "key": "family",
            "title": "Family and Communication",
            "summary": themes["family"],
            "reflection": "What conversation or shared responsibility could benefit from more understanding?",
        },
        {
            "key": "wellbeing",
            "title": "Health and Wellbeing",
            "summary": themes["wellbeing"],
            "reflection": "Which small, sustainable habit could support your everyday wellbeing?",
        },
        {
            "key": "personal_development",
            "title": "Personal Growth",
            "summary": themes["development"],
            "reflection": "What meaningful action could you take this week based on your real circumstances?",
        },
    ]

    # Keep the established four-section interface for existing callers.
    sections = [
        {
            "key": "personality",
            "title": "Personality Themes",
            "summary": themes["personality"],
            "reflection": themes["development"],
        },
        {
            "key": "career",
            "title": "Career and Working Style",
            "summary": themes["career"],
            "reflection": "Which tasks use your skills well, based on your actual experience and interests?",
        },
        {
            "key": "relationships",
            "title": "Relationships and Communication",
            "summary": themes["relationships"],
            "reflection": "What need or expectation could you communicate more clearly in an important relationship?",
        },
        {
            "key": "personal_development",
            "title": "Personal Development",
            "summary": themes["development"],
            "reflection": "Choose one practical goal based on your circumstances, rather than relying on a chart alone.",
        },
    ]

    return {
        "day_master_element": element,
        "strength_category": category,
        "sections": sections,
        "life_sections": life_sections,
        "strength_note": STRENGTH_NOTES[category],
        "element_candidates": candidates,
        "candidate_explanation": (
            "The preliminary method identifies these elements for further "
            f"review: {candidate_text}. They are not definitive favorable "
            "elements or a guaranteed prescription."
        ),
        "development_summary": themes["development"],
        "disclaimer": (
            "BaZi is a traditional Chinese interpretive system, not a "
            "scientifically validated method for predicting personality, "
            "career outcomes, relationships, health, wealth, or future events. "
            "These descriptions are for cultural learning and personal reflection, "
            "not professional advice."
        ),
    }
