from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from machines.models import Machine
from .serializers import MachineSerializer, MachineGuestSerializer

from core.permissions import IsManager
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class MachineViewSet(viewsets.ModelViewSet):
    """
    API для работы с машинами.
    Правила доступа:
    - Менеджер: полный CRUD
    - Клиент: только просмотр своих машин
    - Сервисная организация: просмотр машин своего обслуживания
    """
    serializer_class = MachineSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = [
        'machine_model', 'engine_model', 'transmission_model',
        'steering_axle_model', 'driving_axle_model', 'factory_number'
    ]
    ordering_fields = ['shipment_date']

    def get_permissions(self):
        method = self.request.method

        if method == "DELETE":
            raise PermissionDenied("Удаление машин через API запрещено.")

        if method in ("POST", "PUT", "PATCH"):
            return [IsManager()]

        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = Machine.objects.all().order_by('-shipment_date')

        if not user.is_authenticated:
            return Machine.objects.none()

        if user.groups.filter(name='Клиент').exists():
            return qs.filter(client=user)

        if user.groups.filter(name='Сервисная организация').exists():
            return qs.filter(service_company=user)

        return qs


@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter(
            name="factory_number",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=True,
            description="Заводской номер машины"
        )
    ],
    responses={200: MachineGuestSerializer()}
)


@api_view(['GET'])
@permission_classes([AllowAny])
def machine_search(request):
    factory_number = request.query_params.get('factory_number')

    if not factory_number:
        return Response({"error": "Не указан параметр factory_number"}, status=400)

    try:
        machine = Machine.objects.get(factory_number=factory_number)
    except Machine.DoesNotExist:
        return Response({"error": "Машина не найдена"}, status=404)

    user = request.user

    if user.is_authenticated:

        if user.groups.filter(name="Клиент").exists():
            if machine.client != user:
                return Response({"error": "Нет доступа к этой машине"}, status=403)

        if user.groups.filter(name="Сервисная организация").exists():
            if machine.service_company != user:
                return Response({"error": "Нет доступа к этой машине"}, status=403)

        serializer = MachineSerializer(machine)
        return Response(serializer.data)

    serializer = MachineGuestSerializer(machine)
    return Response(serializer.data)
