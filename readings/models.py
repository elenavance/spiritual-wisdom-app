from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class SpiritualWisdomRating(models.Model):
    RATING_TYPES = [
        ("app", "App experience"),
        ("reading", "Reading"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="spiritual_wisdom_ratings",
    )
    rating_type = models.CharField(max_length=20, choices=RATING_TYPES)
    stars = models.PositiveSmallIntegerField()
    feedback = models.TextField(blank=True, max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} — {self.rating_type}: {self.stars}/5"

    def clean(self):
        from django.core.exceptions import ValidationError

        if not 1 <= self.stars <= 5:
            raise ValidationError({"stars": "Choose between 1 and 5 stars."})
