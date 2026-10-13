from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def validate_birth_timezone(value):
    """Accept valid IANA time-zone identifiers only."""
    if not value:
        return

    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError, TypeError):
        raise ValidationError(
            "Enter a valid time-zone identifier, such as Asia/Jakarta."
        )


class BirthProfile(models.Model):
    GENDER_CHOICES = [
        ("female", "Female"),
        ("male", "Male"),
        ("other", "Other"),
        ("prefer_not_to_say", "Prefer not to say"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="birth_profile",
    )
    display_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
    )
    birth_date = models.DateField()
    birth_time = models.TimeField(blank=True, null=True)
    birth_place = models.CharField(max_length=150, blank=True)
    birth_timezone = models.CharField(
        max_length=64,
        blank=True,
        default="",
        validators=[validate_birth_timezone],
        help_text=(
            "Optional. Choose the time zone where you were born, "
            "if you know it. Example: Asia/Jakarta."
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Birth profile — {self.user.email}"
