from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import SpiritualWisdomRating


@override_settings(STORAGES={"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"}, "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}})
class FeedbackViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="feedback@example.com",
            password="Test-password-482!",
        )

    def test_feedback_requires_login(self):
        response = self.client.get(reverse("readings:feedback"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            reverse("accounts:login"),
            response.url,
        )

    def test_valid_feedback_is_saved(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("readings:feedback"),
            {
                "rating_type": "app",
                "stars": "5",
                "feedback": "A thoughtful experience.",
            },
        )

        self.assertRedirects(response, reverse("readings:feedback"))
        self.assertTrue(
            SpiritualWisdomRating.objects.filter(
                user=self.user,
                rating_type="app",
                stars=5,
                feedback="A thoughtful experience.",
            ).exists()
        )

    def test_invalid_rating_is_rejected(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("readings:feedback"),
            {
                "rating_type": "app",
                "stars": "6",
                "feedback": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(SpiritualWisdomRating.objects.count(), 0)

    def test_invalid_feedback_category_is_rejected(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("readings:feedback"),
            {
                "rating_type": "invalid",
                "stars": "4",
                "feedback": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(SpiritualWisdomRating.objects.count(), 0)

    def test_feedback_over_2000_characters_is_rejected(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("readings:feedback"),
            {
                "rating_type": "reading",
                "stars": "4",
                "feedback": "x" * 2001,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(SpiritualWisdomRating.objects.count(), 0)


class GuestReadingFlowTests(TestCase):
    def test_guest_can_open_preview_form(self):
        response = self.client.get(reverse("readings:preview"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Start with your birth details")

    def test_guest_can_view_result_before_signup(self):
        response = self.client.post(
            reverse("readings:preview"),
            {"birth_date": "1990-05-17", "birth_time": "08:30", "birth_place": "Jakarta"},
        )
        self.assertRedirects(response, reverse("readings:dashboard"))
        result = self.client.get(reverse("readings:dashboard"))
        self.assertEqual(result.status_code, 200)
        self.assertContains(result, "Create an account to save")
        self.assertEqual(self.client.session.get("guest_reading_profile")["birth_date"], "1990-05-17")

    def test_guest_profile_is_saved_when_signup_completes(self):
        self.client.post(
            reverse("readings:preview"),
            {"birth_date": "1990-05-17", "birth_time": "08:30", "birth_place": "Jakarta"},
        )
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "first_name": "New",
                "last_name": "Reader",
                "email": "new-reader@example.com",
                "password1": "Test-password-482!",
                "password2": "Test-password-482!",
            },
        )
        self.assertEqual(response.status_code, 302)
        user = get_user_model().objects.get(email="new-reader@example.com")
        self.assertEqual(user.birth_profile.birth_date.isoformat(), "1990-05-17")
        self.assertEqual(user.birth_profile.birth_place, "Jakarta")
        self.assertNotIn("guest_reading_profile", self.client.session)
