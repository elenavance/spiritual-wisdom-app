
from datetime import date
from types import SimpleNamespace

from django.test import SimpleTestCase
from lunar_python import Solar

from profiles.services.bazi import (
    _get_annual_influences,
    _get_luck_pillars,
    calculate_birth_reading,
)


class LuckPillarsTests(SimpleTestCase):
    def setUp(self):
        solar = Solar.fromYmdHms(1990, 5, 17, 14, 30, 0)
        self.eight_char = solar.getLunar().getEightChar()
        self.eight_char.setSect(2)
        self.day_master = self.eight_char.getDayGan()

    def test_male_profile_returns_forward_luck_pillars(self):
        result = _get_luck_pillars(
            self.eight_char, "male", self.day_master, date(1990, 5, 17)
        )

        self.assertTrue(result["available"])
        self.assertEqual(result["direction"], "Forward")
        self.assertTrue(result["pillars"])
        self.assertTrue(result["start_date"])

    def test_female_profile_returns_backward_luck_pillars(self):
        result = _get_luck_pillars(
            self.eight_char, "female", self.day_master, date(1990, 5, 17)
        )

        self.assertTrue(result["available"])
        self.assertEqual(result["direction"], "Backward")
        self.assertTrue(result["pillars"])

    def test_first_luck_pillar_is_not_blank_preperiod(self):
        for gender in ("male", "female"):
            result = _get_luck_pillars(
                self.eight_char, gender, self.day_master, date(1990, 5, 17)
            )
            self.assertTrue(all(item["gan_zhi"] for item in result["pillars"]))
            self.assertTrue(all(item["index"] > 0 for item in result["pillars"]))

    def test_unknown_gender_does_not_assume_direction(self):
        for gender in ("other", "prefer_not_to_say", None):
            result = _get_luck_pillars(
                self.eight_char, gender, self.day_master, date(1990, 5, 17)
            )
            self.assertFalse(result["available"])
            self.assertIsNone(result["direction"])
            self.assertEqual(result["pillars"], [])

    def test_each_luck_pillar_has_years_ages_and_ten_god(self):
        result = _get_luck_pillars(
            self.eight_char, "male", self.day_master, date(1990, 5, 17)
        )

        for pillar in result["pillars"]:
            with self.subTest(pillar=pillar):
                self.assertIn("gan_zhi", pillar)
                self.assertIn("start_year", pillar)
                self.assertIn("end_year", pillar)
                self.assertIn("start_age", pillar)
                self.assertIn("end_age", pillar)
                self.assertIn("ten_god", pillar)


class AnnualInfluenceTests(SimpleTestCase):
    def test_returns_requested_number_of_years(self):
        result = _get_annual_influences("甲", start_year=2026, count=10)

        self.assertEqual(len(result["years"]), 10)
        self.assertEqual(result["years"][0]["year"], 2026)
        self.assertEqual(result["years"][-1]["year"], 2035)

    def test_annual_influences_have_ganzhi_and_ten_gods(self):
        result = _get_annual_influences("甲", start_year=2026, count=3)

        for item in result["years"]:
            with self.subTest(year=item["year"]):
                self.assertEqual(len(item["gan_zhi"]), 2)
                self.assertTrue(item["element"])
                self.assertTrue(item["ten_god"])
                self.assertTrue(item["ten_god_english"])

    def test_birth_reading_includes_both_new_sections(self):
        profile = SimpleNamespace(
            birth_date=date(1990, 5, 17),
            birth_time=None,
            birth_place="",
            gender="male",
        )

        reading = calculate_birth_reading(profile)

        self.assertIn("luck_pillars", reading)
        self.assertIn("annual_influences", reading)
        self.assertTrue(reading["luck_pillars"]["available"])
        self.assertEqual(len(reading["annual_influences"]["years"]), 10)

    def test_unknown_gender_keeps_annual_influences_available(self):
        profile = SimpleNamespace(
            birth_date=date(1990, 5, 17),
            birth_time=None,
            birth_place="",
            gender="prefer_not_to_say",
        )

        reading = calculate_birth_reading(profile)

        self.assertFalse(reading["luck_pillars"]["available"])
        self.assertEqual(len(reading["annual_influences"]["years"]), 10)
