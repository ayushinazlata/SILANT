from rest_framework import viewsets, filters, permissions
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from .models import Maintenance
from .serializers import MaintenanceSerializer



class MaintenanceViewSet(viewsets.ModelViewSet):
    """
    API для работы с ТО.

    Доступы:
    - Менеджер: CRUD (кроме delete)
    - Клиент: добавление и просмотр своих ТО
    - Сервисная организация: добавление и просмотр ТО своей техники
    """
    
    serializer_class = MaintenanceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = [
        "maintenance_type",
        "machine__factory_number",
        "machine__service_company",
    ]
    ordering_fields = ["maintenance_date"]

    def get_queryset(self):
        user = self.request.user
        qs = Maintenance.objects.all().order_by("-maintenance_date")

        if not user.is_authenticated:
            return Maintenance.objects.none()

        if user.groups.filter(name="Менеджер").exists():
            return qs

        if user.groups.filter(name="Клиент").exists():
            return qs.filter(machine__client=user)

        if user.groups.filter(name="Сервисная организация").exists():
            return qs.filter(machine__service_company=user)

        return Maintenance.objects.none()

    def get_permissions(self):
        if self.request.method == "DELETE":
            raise PermissionDenied("Удаление ТО запрещено.")

        if self.request.method in ("POST", "PATCH", "PUT"):
            return [permissions.IsAuthenticated()]

        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        machine = serializer.validated_data.get("machine")

        if user.groups.filter(name="Менеджер").exists():
            serializer.save()
            return

        if user.groups.filter(name="Клиент").exists() and machine.client != user:
            raise PermissionDenied("Вы можете добавлять ТО только к своим машинам.")

        if user.groups.filter(name="Сервисная организация").exists() and machine.service_company != user:
            raise PermissionDenied("Эта машина обслуживается другой компанией.")

        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user

        if not user.groups.filter(name="Менеджер").exists():
            raise PermissionDenied("Редактировать ТО может только менеджер.")

        return serializer.save()
