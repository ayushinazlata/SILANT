from rest_framework import serializers
from django.core.exceptions import PermissionDenied

from .models import Claim


class ClaimSerializer(serializers.ModelSerializer):

    class Meta:
        model = Claim
        fields = "__all__"

    def validate_operating_time(self, value):
        if value < 0:
            raise serializers.ValidationError("Наработка не может быть отрицательной.")
        return value

    def validate(self, data):
        fd = data.get("failure_date")
        rd = data.get("repair_date")

        if fd and rd and rd < fd:
            raise serializers.ValidationError("Дата восстановления не может быть раньше даты отказа.")

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        machine = validated_data.get("machine")

        if not machine:
            raise PermissionDenied("Машина не выбрана.")

        if user.groups.filter(name="Клиент").exists():
            raise PermissionDenied("Клиенты не могут создавать рекламации.")

        if user.groups.filter(name="Сервисная организация").exists():
            if machine.service_company != user:
                raise PermissionDenied("Эта машина обслуживается другой компанией.")

        validated_data["service_company"] = machine.service_company

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if not user.groups.filter(name="Менеджер").exists():
            raise PermissionDenied("Редактировать рекламацию может только менеджер.")
        return super().update(instance, validated_data)
