from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from profiles.models import BirthProfile

from .forms import SignupForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("profiles:edit_profile")

    next_url = request.POST.get("next_url") or request.GET.get("next", "")
    if not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = ""

    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        guest_data = request.session.pop("guest_reading_profile", None)
        saved_guest_profile = False
        if isinstance(guest_data, dict):
            try:
                BirthProfile.objects.create(
                    user=user,
                    display_name=guest_data.get("display_name", ""),
                    gender=guest_data.get("gender", ""),
                    birth_date=guest_data["birth_date"],
                    birth_time=guest_data.get("birth_time") or None,
                    birth_place=guest_data.get("birth_place", ""),
                    birth_timezone=guest_data.get("birth_timezone", ""),
                )
                saved_guest_profile = True
            except (KeyError, TypeError, ValueError):
                request.session["guest_reading_profile"] = guest_data
        login(request, user)
        messages.success(request, "Your account has been created.")
        if saved_guest_profile:
            return redirect("readings:dashboard")
        return redirect(next_url or "profiles:edit_profile")

    return render(
        request,
        "accounts/signup.html",
        {"form": form, "next_url": next_url},
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("profiles:edit_profile")

    form = AuthenticationForm(request, data=request.POST or None)
    form.fields["username"].label = "Email address"
    form.fields["username"].widget.attrs.update({
        "type": "email",
        "autocomplete": "email",
    })

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("profiles:edit_profile")

    return render(request, "accounts/login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("profiles:home")
