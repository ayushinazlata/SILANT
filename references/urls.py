from django.urls import path
from . import views


urlpatterns = [
    path("", views.reference_all_view, name="reference-all"),
    path("create/<slug:model_name>/", views.reference_create, name="reference-create"),
    path("<slug:model_name>/<int:pk>/", views.reference_detail, name="reference-detail"),
]
