from django.urls import path

from . import views

app_name = "readings"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]
