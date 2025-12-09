from django.urls import path
from .views import ClaimCreateView


urlpatterns = [
    path("create/", ClaimCreateView.as_view(), name="create-claim"),
    path("create/<int:pk>/", ClaimCreateView.as_view(), name="create-claim-for-machine"),
]
