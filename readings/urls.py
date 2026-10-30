from django.urls import path

from . import (
    compatibility_views,
    feedback_views,
    other_person_views,
    views,
)

app_name = "readings"

urlpatterns = [
    path("preview/", views.preview, name="preview"),
    path("feedback/", feedback_views.feedback, name="feedback"),
    path(
        "love-compatibility/",
        compatibility_views.love_compatibility,
        name="love_compatibility",
    ),
    path(
        "test-another-person/",
        other_person_views.test_another_person,
        name="test_another_person",
    ),
    path("", views.dashboard, name="dashboard"),
]
