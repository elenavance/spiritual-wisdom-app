from zoneinfo import available_timezones

from django import forms

from .models import BirthProfile


TIMEZONE_CHOICES = [("", "Select if known")] + [
    (zone, zone) for zone in sorted(available_timezones())
]


class BirthProfileForm(forms.ModelForm):
    birth_timezone = forms.ChoiceField(
        label="Birth time zone",
        choices=TIMEZONE_CHOICES,
        required=False,
        help_text=(
            "Optional. Select the time zone where you were born, "
            "if known. This records the zone but does not yet "
            "automatically correct the chart for historical time rules."
        ),
        widget=forms.Select(),
    )

    class Meta:
        model = BirthProfile
        fields = (
            "display_name",
            "gender",
            "birth_date",
            "birth_time",
            "birth_place",
            "birth_timezone",
        )
        widgets = {
            "display_name": forms.TextInput(
                attrs={"autocomplete": "name"}
            ),
            "birth_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "birth_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
            "birth_place": forms.TextInput(
                attrs={
                    "placeholder": "City and country (optional)"
                }
            ),
        }
