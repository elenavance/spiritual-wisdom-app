from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import SignupForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("profiles:edit_profile")

    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("profiles:edit_profile")

    return render(request, "accounts/signup.html", {"form": form})


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
