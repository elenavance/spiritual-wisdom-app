
from django.test import SimpleTestCase
from lunar_python import Solar


def get_pillars(year, month, day, hour=12, minute=0):
    solar = Solar.fromYmdHms(
        year, month, day, hour, minute, 0
    )
    eight_char = solar.getLunar().getEightChar()
    eight_char.setSect(2)

    return {
        "year": eight_char.getYear(),
        "month": eight_char.getMonth(),
        "day": eight_char.getDay(),
    }


class SolarTermBoundaryTests(SimpleTestCase):
    def test_before_lichun_uses_previous_bazi_year(self):
        pillars = get_pillars(2024, 2, 3)

        self.assertEqual(pillars["year"], "癸卯")

    def test_after_lichun_uses_new_bazi_year(self):
        pillars = get_pillars(2024, 2, 5)

        self.assertEqual(pillars["year"], "甲辰")

    def test_february_four_exact_boundary_result_is_preserved(self):
        # At noon, the library's exact method returns 癸卯 for this date.
        pillars = get_pillars(2024, 2, 4)

        self.assertEqual(pillars["year"], "癸卯")

    def test_before_jingzhe_uses_yin_month(self):
        pillars = get_pillars(2024, 3, 4)

        self.assertEqual(pillars["month"], "丙寅")

    def test_after_jingzhe_uses_mao_month(self):
        pillars = get_pillars(2024, 3, 6)

        self.assertEqual(pillars["month"], "丁卯")

    def test_month_boundary_day_pillar_is_still_calculated(self):
        pillars = get_pillars(2024, 3, 5)

        self.assertEqual(pillars["month"], "丁卯")
        self.assertEqual(pillars["day"], "戊辰")
