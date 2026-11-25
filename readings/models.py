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

from django.core.validators import MinValueValidator, MaxValueValidator

class BuddhistWisdom(models.Model):
    day_index = models.IntegerField(unique=True)  # 0-29
    title = models.CharField(max_length=120)
    text = models.TextField()
    practice = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Rating(models.Model):
    READING_TYPES = [
        ('bazi', 'BaZi'),
        ('zodiac', 'Zodiac'),
        ('five_elements', 'Five Elements'),
        ('love', 'Love Compatibility'),
        ('buddhist', 'Buddhist Wisdom'),
        ('general', 'General'),
    ]
    user = models.ForeignKey(
        'auth.User', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='ratings'
    )
    nickname = models.CharField(max_length=30, blank=True)
    stars = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(max_length=500, blank=True)
    reading_type = models.CharField(max_length=30, choices=READING_TYPES, default='general')
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
