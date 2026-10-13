from django.contrib import admin
from django.urls import include, path

from profiles import pwa_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("service-worker.js", pwa_views.service_worker, name="service_worker"),
    path("offline/", pwa_views.offline, name="offline"),
    path("my-readings/", include("readings.urls")),
    path("", include("profiles.urls")),
]
