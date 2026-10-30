from calendar import monthrange
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


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



class VipTrial(models.Model):
    """A one-time, user-started, no-payment one-calendar-month trial."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vip_trial",
    )
    activated_at = models.DateTimeField(default=timezone.now)

    @property
    def ends_at(self):
        month = self.activated_at.month % 12 + 1
        year = self.activated_at.year + (1 if self.activated_at.month == 12 else 0)
        day = min(self.activated_at.day, monthrange(year, month)[1])
        return self.activated_at.replace(year=year, month=month, day=day)

    def is_active(self, at=None):
        return (at or timezone.now()) < self.ends_at


def user_has_active_vip(user, at=None):
    if not getattr(user, "is_authenticated", False):
        return False
    try:
        return user.vip_trial.is_active(at)
    except VipTrial.DoesNotExist:
        return False
