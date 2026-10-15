from datetime import date, time
from types import SimpleNamespace

from django.test import SimpleTestCase

from profiles.services.chart_analysis import build_chart_analysis


class ChartAnalysisIntegrationTests(SimpleTestCase):
    def test_chart_analysis_without_birth_time(self):
        profile = SimpleNamespace(
            birth_date=date(1990, 6, 15),
            birth_time=None,
        )

        result = build_chart_analysis(profile)

        self.assertFalse(result["has_hour_pillar"])
        self.assertIn("strength", result)
        self.assertIn("useful_elements", result)
        self.assertIn("interpretation", result)
        self.assertTrue(result["useful_elements"]["not_a_definitive_yong_shen"])
        self.assertEqual(len(result["interpretation"]["sections"]), 4)

    def test_chart_analysis_with_birth_time(self):
        profile = SimpleNamespace(
            birth_date=date(1990, 6, 15),
            birth_time=time(12, 0),
        )

        result = build_chart_analysis(profile)

        self.assertTrue(result["has_hour_pillar"])
        self.assertEqual(len(result["interpretation"]["sections"]), 4)
