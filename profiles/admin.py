from django.contrib import admin
from .models import BirthProfile


@admin.register(BirthProfile)
class BirthProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "birth_date", "gender", "birth_place", "updated_at")
    search_fields = ("user__email", "display_name", "birth_place")
    list_filter = ("gender",)
