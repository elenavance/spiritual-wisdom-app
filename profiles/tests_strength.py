
from django.test import SimpleTestCase
from lunar_python import Solar

from profiles.services.strength import analyze_day_master_strength
from profiles.services.useful_elements import analyze_useful_elements


class DayMasterStrengthTests(SimpleTestCase):
    def make_chart(self, year, month, day, hour=12):
        solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        chart = solar.getLunar().getEightChar()
        chart.setSect(2)
        return chart

    def test_strength_returns_required_explanation_fields(self):
        result = analyze_day_master_strength(self.make_chart(1990, 5, 17))
        self.assertIn(result["category"], {"weak", "balanced", "strong"})
        self.assertIn("day_master_element", result)
        self.assertIn("support_score", result)
        self.assertIn("pressure_score", result)
        self.assertIn("support_ratio", result)
        self.assertIn("root_count", result)
        self.assertTrue(result["method"])
        self.assertTrue(result["pillars"])

    def test_strength_ratio_is_bounded(self):
        result = analyze_day_master_strength(self.make_chart(2000, 1, 1))
        self.assertGreaterEqual(result["support_ratio"], 0)
        self.assertLessEqual(result["support_ratio"], 1)

    def test_hour_can_be_excluded(self):
        chart = self.make_chart(1990, 5, 17)
        result = analyze_day_master_strength(chart, include_hour=False)
        self.assertEqual(
            [p["pillar"] for p in result["pillars"]],
            ["Year", "Month", "Day"],
        )

    def test_useful_element_candidates_are_provisional(self):
        strength = analyze_day_master_strength(self.make_chart(1990, 5, 17))
        result = analyze_useful_elements(strength)

        self.assertEqual(result["status"], "provisional")
        self.assertTrue(result["not_a_definitive_yong_shen"])
        self.assertTrue(result["primary_candidates"])
        self.assertTrue(result["limitations"])

    def test_all_strength_categories_are_supported(self):
        for category in ("weak", "balanced", "strong"):
            result = analyze_useful_elements({
                "day_master_element": "Wood",
                "category": category,
            })
            self.assertTrue(result["primary_candidates"])
            self.assertTrue(result["secondary_candidates"])
