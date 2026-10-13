from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("", views.home, name="home"),
    path("my-profile/", views.edit_profile, name="edit"),
]
