from django.urls import path
from .views import MachineCreateView, MachineDetailView, machine_search_view


urlpatterns = [
    path('', machine_search_view, name='home'),
    path("machines/<int:pk>/", MachineDetailView.as_view(), name="machine-detail"),
    path("create/", MachineCreateView.as_view(), name="machine-create"),
]
