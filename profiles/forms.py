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

    def __init__(self, *args, language="en", **kwargs):
        super().__init__(*args, **kwargs)

        if language == "zh":
            labels = {
                "display_name": "显示名称",
                "gender": "性别",
                "birth_date": "出生日期",
                "birth_time": "出生时间",
                "birth_place": "出生地点",
                "birth_timezone": "出生时区",
            }
            for field, label in labels.items():
                if field in self.fields:
                    self.fields[field].label = label

            self.fields["birth_timezone"].help_text = (
                "选填。如果知道，"
                "请选择出生地的时区。"
                "此设置目前仅记录时区，"
                "尚未自动校正历史时区规则。"
            )
            self.fields["birth_timezone"].choices = [
                ("", "如知道请选择")
            ] + [(zone, zone) for zone in sorted(available_timezones())]
            self.fields["birth_place"].widget.attrs["placeholder"] = (
                "城市和国家（选填）"
            )
        else:
            self.fields["birth_timezone"].choices = TIMEZONE_CHOICES

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
                attrs={"placeholder": "City and country (optional)"}
            ),
        }
