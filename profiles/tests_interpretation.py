
from django.test import SimpleTestCase

from profiles.services.interpretation import (
    ELEMENT_THEMES,
    generate_chart_interpretation,
)


class ChartInterpretationTests(SimpleTestCase):
    def test_every_element_has_all_four_topics(self):
        for element, themes in ELEMENT_THEMES.items():
            with self.subTest(element=element):
                for topic in (
                    "personality",
                    "career",
                    "relationships",
                    "development",
                ):
                    self.assertTrue(themes[topic])

    def test_interpretation_has_four_sections(self):
        strength = {
            "day_master_element": "Wood",
            "category": "balanced",
        }
        useful = {
            "primary_candidates": ["Fire", "Water"],
            "status": "provisional",
        }

        result = generate_chart_interpretation(strength, useful)

        self.assertEqual(len(result["sections"]), 4)
        self.assertEqual(
            [section["key"] for section in result["sections"]],
            [
                "personality",
                "career",
                "relationships",
                "personal_development",
            ],
        )

    def test_interpretation_mentions_uncertainty(self):
        result = generate_chart_interpretation(
            {"day_master_element": "Fire", "category": "strong"},
            {"primary_candidates": ["Earth", "Metal"]},
        )

        self.assertTrue(result["strength_note"])
        self.assertIn("not definitive", result["candidate_explanation"])
        self.assertIn("not a scientifically validated", result["disclaimer"])

    def test_invalid_element_is_rejected(self):
        with self.assertRaises(ValueError):
            generate_chart_interpretation(
                {"day_master_element": "Lightning", "category": "strong"},
                {"primary_candidates": []},
            )

    def test_invalid_strength_category_is_rejected(self):
        with self.assertRaises(ValueError):
            generate_chart_interpretation(
                {"day_master_element": "Wood", "category": "certain"},
                {"primary_candidates": []},
            )
