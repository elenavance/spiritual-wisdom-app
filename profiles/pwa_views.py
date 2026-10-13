from pathlib import Path

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render


def offline(request):
    return render(request, "pwa/offline.html")


def service_worker(request):
    worker_path = Path(settings.BASE_DIR) / "static" / "pwa" / "service-worker.js"
    response = FileResponse(
        worker_path.open("rb"),
        content_type="application/javascript; charset=utf-8",
    )
    response["Service-Worker-Allowed"] = "/"
    response["Cache-Control"] = "no-cache"
    return response
