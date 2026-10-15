from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

SUPPORTED_LANGUAGES = {"en", "zh"}


@require_POST
def set_language(request):
    language = request.POST.get("language", "en").strip().lower()

    if language not in SUPPORTED_LANGUAGES:
        language = "en"

    request.session["app_language"] = language

    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER", "/")

    if not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = "/"

    return redirect(next_url)
