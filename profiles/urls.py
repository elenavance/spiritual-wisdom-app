from django.urls import path

from . import feature_views, language_views, lucky_views, views

app_name = "profiles"

urlpatterns = [
    path("", views.home, name="home"),
    path("my-profile/", views.edit_profile, name="edit_profile"),
    path("set-language/", language_views.set_language, name="set_language"),
    path("features/", feature_views.features, name="features"),
    path("ask-me/", feature_views.ask_me, name="ask_me"),
    path("vip/", feature_views.vip_membership, name="vip"),
    path("lucky-color-number/", lucky_views.lucky_color_number, name="lucky_color_number"),
]
