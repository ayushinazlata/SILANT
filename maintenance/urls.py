from django.urls import path
from .views import MaintenanceCreateView


urlpatterns = [
    path("create/", MaintenanceCreateView.as_view(), name="maintenance-create"),
    path("create/<int:pk>/", MaintenanceCreateView.as_view(), name="maintenance-create-by-machine"),
]
