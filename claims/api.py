from rest_framework import viewsets, filters, permissions
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from core.permissions import IsManager
from .models import Claim
from .serializers import ClaimSerializer


class ClaimViewSet(viewsets.ModelViewSet):
    """
    API для работы с рекламациями.

    Доступы:
    - Менеджер: полный CRUD (кроме delete)
    - Сервисная организация: создание рекламаций по своим машинам
    - Клиент: только просмотр рекламаций своих машин
    """
    
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["failure_node", "recovery_method"]
    ordering_fields = ["failure_date"]

    def get_permissions(self):
        if self.request.method in ("POST", "PUT", "PATCH"):
            return [IsManager()]
        elif self.request.method == "DELETE":
            raise PermissionDenied("Удаление рекламаций запрещено.")
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Claim.objects.none()

        qs = Claim.objects.all().order_by("-failure_date")

        if user.groups.filter(name="Менеджер").exists():
            return qs

        if user.groups.filter(name="Клиент").exists():
            return qs.filter(machine__client=user)

        if user.groups.filter(name="Сервисная организация").exists():
            return qs.filter(machine__service_company=user)

        return Claim.objects.none()
