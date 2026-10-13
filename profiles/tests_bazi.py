
from django.test import SimpleTestCase
from lunar_python import Solar

from profiles.services.bazi import ten_god_for_stem
from profiles.services.elements import analyze_five_elements


class TenGodCalculationTests(SimpleTestCase):
    """Check all ten stem relationships against a 甲 Wood Day Master."""

    def test_all_ten_gods_for_jia_wood_day_master(self):
        expected = {
            "甲": "比肩",  # Friend
            "乙": "劫财",  # Rob Wealth
            "丙": "食神",  # Eating God
            "丁": "伤官",  # Hurting Officer
            "戊": "偏财",  # Indirect Wealth
            "己": "正财",  # Direct Wealth
            "庚": "七杀",  # Seven Killings
            "辛": "正官",  # Direct Officer
            "壬": "偏印",  # Indirect Resource
            "癸": "正印",  # Direct Resource
        }

        for stem, expected_god in expected.items():
            with self.subTest(stem=stem):
                self.assertEqual(
                    ten_god_for_stem("甲", stem),
                    expected_god,
                )

    def test_same_stem_is_friend(self):
        self.assertEqual(ten_god_for_stem("甲", "甲"), "比肩")

    def test_opposite_polarity_same_element_is_rob_wealth(self):
        self.assertEqual(ten_god_for_stem("甲", "乙"), "劫财")


class HiddenStemAndFiveElementTests(SimpleTestCase):
    def setUp(self):
        # Fixed sample birth data makes these tests repeatable.
        solar = Solar.fromYmdHms(1990, 5, 17, 14, 30, 0)
        self.eight_char = solar.getLunar().getEightChar()

    def test_pillars_include_hidden_stem_details(self):
        result = analyze_five_elements(
            self.eight_char,
            include_hour=True,
        )

        self.assertEqual(len(result["pillars"]), 4)

        for pillar in result["pillars"]:
            with self.subTest(pillar=pillar["pillar"]):
                self.assertIn("hidden_stems", pillar)
                self.assertIn("hidden_details", pillar)

                self.assertEqual(
                    len(pillar["hidden_stems"]),
                    len(pillar["hidden_details"]),
                )

                for detail in pillar["hidden_details"]:
                    self.assertIn("stem", detail)
                    self.assertIn("element", detail)
                    self.assertIn("element_english", detail)

    def test_hidden_stem_counts_match_pillar_details(self):
        result = analyze_five_elements(
            self.eight_char,
            include_hour=True,
        )

        observed = {
            element: 0 for element in result["elements"]
        }

        for pillar in result["pillars"]:
            for detail in pillar["hidden_details"]:
                observed[detail["element"]] += 1

        self.assertEqual(
            observed,
            result["hidden_stem_counts"],
        )

    def test_without_birth_time_omits_hour_pillar(self):
        result = analyze_five_elements(
            self.eight_char,
            include_hour=False,
        )

        self.assertFalse(result["has_hour_pillar"])
        self.assertEqual(len(result["pillars"]), 3)
        self.assertEqual(
            [pillar["pillar"] for pillar in result["pillars"]],
            ["Year", "Month", "Day"],
        )

    def test_structural_totals_and_percentages_are_consistent(self):
        result = analyze_five_elements(
            self.eight_char,
            include_hour=True,
        )

        for element in result["elements"]:
            with self.subTest(element=element):
                expected_total = (
                    result["visible_stem_counts"][element]
                    + result["branch_element_counts"][element]
                    + result["hidden_stem_counts"][element]
                )

                self.assertEqual(
                    result["structural_totals"][element],
                    expected_total,
                )

        self.assertEqual(
            sum(result["structural_totals"].values()),
            result["total_occurrences"],
        )

        if result["total_occurrences"]:
            for element in result["elements"]:
                expected_percentage = round(
                    result["structural_totals"][element]
                    / result["total_occurrences"]
                    * 100,
                    1,
                )
                self.assertEqual(
                    result["structural_percentages"][element],
                    expected_percentage,
                )
