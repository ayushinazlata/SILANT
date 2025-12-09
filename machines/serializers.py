from rest_framework import serializers
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from .models import Machine
from references.serializers import (
    MachineModelSerializer,
    EngineModelSerializer,
    TransmissionModelSerializer,
    DrivingAxleModelSerializer,
    SteeringAxleModelSerializer,
)




class MachineSerializer(serializers.ModelSerializer):
    machine_model = MachineModelSerializer(read_only=True)
    engine_model = EngineModelSerializer(read_only=True)
    transmission_model = TransmissionModelSerializer(read_only=True)
    driving_axle_model = DrivingAxleModelSerializer(read_only=True)
    steering_axle_model = SteeringAxleModelSerializer(read_only=True)

    client = serializers.StringRelatedField(read_only=True)
    service_company = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Machine
        fields = "__all__"

    def validate_factory_number(self, value):
        qs = Machine.objects.filter(factory_number=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Машина с таким заводским номером уже существует.")
        return value

    def validate_shipment_date(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Дата отгрузки не может быть в будущем.")
        return value

    def validate(self, data):
        user = self.context["request"].user

        if user.groups.filter(name="Менеджер").exists():
            return data

        restricted_fields = ("client", "service_company")

        for field in restricted_fields:
            if field in data:
                raise serializers.ValidationError("Вы не можете изменять поле: %s" % field)

        return data

    def create(self, validated_data):
        user = self.context["request"].user

        if not user.groups.filter(name="Менеджер").exists():
            raise PermissionDenied("Создание машин доступно только менеджеру.")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user

        if not user.groups.filter(name="Менеджер").exists():
            raise PermissionDenied("Редактирование машин доступно только менеджеру.")

        return super().update(instance, validated_data)



class MachineGuestSerializer(serializers.ModelSerializer):
    machine_model = MachineModelSerializer(read_only=True)
    engine_model = EngineModelSerializer(read_only=True)
    transmission_model = TransmissionModelSerializer(read_only=True)
    driving_axle_model = DrivingAxleModelSerializer(read_only=True)
    steering_axle_model = SteeringAxleModelSerializer(read_only=True)

    class Meta:
        model = Machine
        fields = [
            "factory_number",
            "machine_model",
            "engine_model",
            "engine_number",
            "transmission_model",
            "transmission_number",
            "driving_axle_model",
            "driving_axle_number",
            "steering_axle_model",
            "steering_axle_number",
        ]
