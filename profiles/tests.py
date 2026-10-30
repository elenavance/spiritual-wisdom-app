from datetime import date, datetime, time, timezone as datetime_timezone
from types import SimpleNamespace

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from lunar_python import Solar

from profiles.forms import BirthProfileForm
from profiles.models import VipTrial, user_has_active_vip, validate_birth_timezone
from profiles.services.bazi import calculate_birth_reading


class CalendarBoundaryTests(SimpleTestCase):
    """Verify calendar boundaries and the chosen Day Pillar convention."""

    def test_zodiac_changes_at_lunar_new_year(self):
        before_new_year = Solar.fromYmdHms(2024, 2, 9, 12, 0, 0)
        on_new_year = Solar.fromYmdHms(2024, 2, 10, 12, 0, 0)

        self.assertEqual(
            before_new_year.getLunar().getYearShengXiao(), "兔"
        )
        self.assertEqual(
            on_new_year.getLunar().getYearShengXiao(), "龙"
        )

    def test_bazi_year_changes_at_li_chun(self):
        before_li_chun = Solar.fromYmdHms(2024, 2, 4, 16, 0, 0)
        after_li_chun = Solar.fromYmdHms(2024, 2, 4, 17, 0, 0)

        self.assertEqual(
            before_li_chun.getLunar().getEightChar().getYear(), "癸卯"
        )
        self.assertEqual(
            after_li_chun.getLunar().getEightChar().getYear(), "甲辰"
        )

    def test_reading_service_uses_bazi_year_boundary(self):
        profile_before = SimpleNamespace(
            birth_date=date(2024, 2, 4),
            birth_time=time(16, 0),
            birth_place="Jakarta, Indonesia",
        )
        profile_after = SimpleNamespace(
            birth_date=date(2024, 2, 4),
            birth_time=time(17, 0),
            birth_place="Jakarta, Indonesia",
        )

        reading_before = calculate_birth_reading(profile_before)
        reading_after = calculate_birth_reading(profile_after)

        self.assertEqual(reading_before["pillars"][0]["chinese"], "癸卯")
        self.assertEqual(reading_after["pillars"][0]["chinese"], "甲辰")
        self.assertEqual(reading_before["zodiac"]["chinese"], "兔")
        self.assertEqual(reading_after["zodiac"]["chinese"], "兔")

    def test_sect_2_day_pillar_before_midnight(self):
        profile = SimpleNamespace(
            birth_date=date(2024, 1, 15),
            birth_time=time(23, 30),
            birth_place="Jakarta, Indonesia",
        )

        reading = calculate_birth_reading(profile)
        pillars = {pillar["name"]: pillar["chinese"]
                   for pillar in reading["pillars"]}

        self.assertEqual(pillars["Day"], "戊寅")
        self.assertEqual(pillars["Hour"], "甲子")

    def test_day_pillar_changes_at_midnight_under_sect_2(self):
        profile = SimpleNamespace(
            birth_date=date(2024, 1, 16),
            birth_time=time(0, 0),
            birth_place="Jakarta, Indonesia",
        )

        reading = calculate_birth_reading(profile)
        pillars = {pillar["name"]: pillar["chinese"]
                   for pillar in reading["pillars"]}

        self.assertEqual(pillars["Day"], "己卯")
        self.assertEqual(pillars["Hour"], "甲子")

    def test_missing_birth_time_omits_hour_pillar(self):
        profile = SimpleNamespace(
            birth_date=date(1996, 11, 15),
            birth_time=None,
            birth_place="Jakarta, Indonesia",
        )

        reading = calculate_birth_reading(profile)

        self.assertFalse(reading["birth_time_known"])
        self.assertFalse(reading["is_full_four_pillars"])
        self.assertEqual(
            [pillar["name"] for pillar in reading["pillars"]],
            ["Year", "Month", "Day"],
        )
        self.assertTrue(reading["warnings"])

    def test_missing_birth_date_raises_error(self):
        profile = SimpleNamespace(
            birth_date=None,
            birth_time=None,
            birth_place="Jakarta, Indonesia",
        )

        with self.assertRaises(ValueError):
            calculate_birth_reading(profile)


class BirthTimezoneValidationTests(SimpleTestCase):
    """Verify the optional time-zone identifier validation."""

    def test_accepts_valid_timezone(self):
        validate_birth_timezone("Asia/Jakarta")

    def test_rejects_invalid_timezone(self):
        with self.assertRaises(ValidationError):
            validate_birth_timezone("Not/A_Real_Timezone")

    def test_accepts_blank_optional_timezone(self):
        validate_birth_timezone("")

    def test_form_includes_optional_timezone_field(self):
        form = BirthProfileForm()

        self.assertIn("birth_timezone", form.fields)
        self.assertFalse(form.fields["birth_timezone"].required)



@override_settings(STORAGES={"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"}, "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}})
class VipTrialTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="vip-trial@example.com",
            password="SecureTestPass_482!",
        )
        self.client.force_login(self.user)

    def test_account_creation_does_not_start_vip_trial(self):
        self.assertFalse(VipTrial.objects.filter(user=self.user).exists())
        self.assertFalse(user_has_active_vip(self.user))

    def test_user_can_start_one_trial_without_a_payment_method(self):
        page = self.client.get(reverse("profiles:vip"))
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "No payment method is required")
        self.assertContains(page, "Start my free VIP month")
        self.assertFalse(user_has_active_vip(self.user))

        response = self.client.post(reverse("profiles:vip"))
        self.assertRedirects(response, reverse("profiles:vip"))
        trial = VipTrial.objects.get(user=self.user)
        self.assertTrue(trial.is_active())
        self.assertTrue(user_has_active_vip(self.user))
        self.assertGreaterEqual(trial.activated_at, self.user.date_joined)

    def test_repeated_start_does_not_reset_trial(self):
        self.client.post(reverse("profiles:vip"))
        original_start = VipTrial.objects.get(user=self.user).activated_at
        self.client.post(reverse("profiles:vip"))
        self.assertEqual(VipTrial.objects.get(user=self.user).activated_at, original_start)
        self.assertEqual(VipTrial.objects.count(), 1)

    def test_trial_ends_on_same_calendar_day_next_month(self):
        trial = VipTrial(
            user=self.user,
            activated_at=datetime(2024, 1, 31, 12, 0, tzinfo=datetime_timezone.utc),
        )
        self.assertEqual(
            trial.ends_at,
            datetime(2024, 2, 29, 12, 0, tzinfo=datetime_timezone.utc),
        )
        self.assertTrue(trial.is_active(datetime(2024, 2, 29, 11, 59, tzinfo=datetime_timezone.utc)))
        self.assertFalse(trial.is_active(trial.ends_at))

    def test_expired_trial_does_not_grant_vip_access(self):
        trial = VipTrial.objects.create(
            user=self.user,
            activated_at=datetime(2024, 1, 31, 12, 0, tzinfo=datetime_timezone.utc),
        )
        self.assertFalse(trial.is_active(datetime(2024, 3, 1, 12, 0, tzinfo=datetime_timezone.utc)))
