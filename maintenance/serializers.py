from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from .models import Maintenance
from machines.models import Machine



class MaintenanceSerializer(serializers.ModelSerializer):
    machine = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.none()
    )

    class Meta:
        model = Maintenance
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        user = kwargs["context"]["request"].user
        super().__init__(*args, **kwargs)

        if user.groups.filter(name="Менеджер").exists():
            self.fields["machine"].queryset = Machine.objects.all()

        elif user.groups.filter(name="Клиент").exists():
            self.fields["machine"].queryset = Machine.objects.filter(client=user)

        elif user.groups.filter(name="Сервисная организация").exists():
            self.fields["machine"].queryset = Machine.objects.filter(service_company=user)

    def validate_operating_time(self, value):
        if value < 0:
            raise serializers.ValidationError("Наработка не может быть отрицательной.")
        return value

    def validate(self, data):
        order_date = data.get("order_date")
        maintenance_date = data.get("maintenance_date")
        today = timezone.now().date()

        if order_date and order_date > today:
            raise serializers.ValidationError("Дата заказ-наряда не может быть в будущем.")

        if maintenance_date and maintenance_date > today:
            raise serializers.ValidationError("Дата проведения ТО не может быть в будущем.")

        if order_date and maintenance_date and maintenance_date < order_date:
            raise serializers.ValidationError("Дата проведения ТО не может быть раньше заказ-наряда.")

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        machine = validated_data.get("machine")

        if not machine:
            raise PermissionDenied("Выберите машину.")

        if user.groups.filter(name="Клиент").exists():
            if machine.client != user:
                raise PermissionDenied("Вы можете добавлять ТО только к своим машинам.")

        if user.groups.filter(name="Сервисная организация").exists():
            if machine.service_company != user:
                raise PermissionDenied("Вы можете добавлять ТО только к машинам вашей компании.")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if not user.groups.filter(name="Менеджер").exists():
            raise PermissionDenied("Редактировать ТО может только менеджер.")
        return super().update(instance, validated_data)
