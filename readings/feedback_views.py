from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods

from .models import SpiritualWisdomRating


@login_required
@require_http_methods(["GET", "POST"])
def feedback(request):
    if request.method == "POST":
        rating_type = request.POST.get("rating_type", "app")
        stars_text = request.POST.get("stars", "")
        comment = request.POST.get("feedback", "").strip()
        next_url = request.POST.get("next", "")

        if rating_type not in {"app", "reading"}:
            messages.error(request, "Please choose a valid feedback category.")
        elif not stars_text.isdigit() or not 1 <= int(stars_text) <= 5:
            messages.error(request, "Please select a rating from 1 to 5 stars.")
        elif len(comment) > 2000:
            messages.error(request, "Feedback must be 2,000 characters or fewer.")
        else:
            SpiritualWisdomRating.objects.create(
                user=request.user,
                rating_type=rating_type,
                stars=int(stars_text),
                feedback=comment,
            )
            messages.success(request, "Thank you for sharing your feedback.")

            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect("readings:feedback")

    return render(request, "readings/feedback.html")
