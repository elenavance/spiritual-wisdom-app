from django.test import TestCase, override_settings
from django.urls import reverse


TEST_STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
}


@override_settings(STORAGES=TEST_STORAGES)
class GuestBaZiTests(TestCase):
    def test_guest_calculator_is_public(self):
        response = self.client.get(reverse("profiles:guest_bazi"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Calculate My Free BaZi Chart")

    def test_guest_can_calculate_once_without_creating_account(self):
        response = self.client.post(
            reverse("profiles:guest_bazi"),
            {
                "birth_date": "1990-05-17",
                "birth_time": "08:30",
                "gender": "female",
                "birth_place": "Jakarta, Indonesia",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your BaZi Overview")
        self.assertContains(response, "Four Pillars")
        self.assertTrue(self.client.session.get("guest_bazi_used"))
        self.assertIn("guest_bazi_result", self.client.session)
        self.assertFalse(self.client.session.get("_auth_user_id"))

    def test_guest_cannot_submit_a_second_calculation_in_same_session(self):
        url = reverse("profiles:guest_bazi")
        payload = {
            "birth_date": "1990-05-17",
            "birth_time": "08:30",
            "gender": "",
            "birth_place": "",
        }
        first = self.client.post(url, payload)
        self.assertEqual(first.status_code, 200)
        first_day_master = self.client.session["guest_bazi_result"]["reading"]["day_master"]

        second = self.client.post(
            url,
            {
                "birth_date": "2000-01-01",
                "birth_time": "12:00",
                "gender": "",
                "birth_place": "",
            },
            follow=True,
        )
        self.assertEqual(second.status_code, 200)
        self.assertContains(second, "already been used")
        self.assertEqual(
            self.client.session["guest_bazi_result"]["reading"]["day_master"],
            first_day_master,
        )

    def test_invalid_guest_form_does_not_consume_free_calculation(self):
        response = self.client.post(
            reverse("profiles:guest_bazi"),
            {"birth_date": "not-a-date", "birth_time": "", "gender": "", "birth_place": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.client.session.get("guest_bazi_used"))

    def test_mobile_app_navigation_is_available_to_guests(self):
        response = self.client.get(reverse("profiles:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aria-label="Main app navigation"')
        self.assertContains(response, reverse("profiles:guest_bazi"))
        self.assertContains(response, reverse("profiles:buddhist_wisdom"))

    def test_buddhist_wisdom_is_public(self):
        response = self.client.get(reverse("profiles:buddhist_wisdom"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Four Noble Truths")
        self.assertContains(response, "SN 56.11")
