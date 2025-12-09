from django.http import JsonResponse
from django.shortcuts import render


def custom_403(request, exception=None):
    if request.path.startswith("/api/"):
        return JsonResponse(
            {"detail": "У вас нет прав для выполнения этой операции."},
            status=403
        )

    return render(request, "errors/403.html", status=403)


def custom_404(request, exception):
    return render(request, "errors/404.html", status=404)


def custom_500(request):
    return render(request, "errors/500.html", status=500)
