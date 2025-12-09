from rest_framework import serializers


class ReferenceBaseSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор справочников: выводит id и name.
    Meta.model задаётся в наследниках.
    """
    class Meta:
        fields = ["id", "name"]


from .models import (
    MachineModel,
    EngineModel,
    TransmissionModel,
    DrivingAxleModel,
    SteeringAxleModel,
)
from rest_framework import serializers
from .serializers import ReferenceBaseSerializer


class MachineModelSerializer(ReferenceBaseSerializer):
    class Meta(ReferenceBaseSerializer.Meta):
        model = MachineModel


class EngineModelSerializer(ReferenceBaseSerializer):
    class Meta(ReferenceBaseSerializer.Meta):
        model = EngineModel


class TransmissionModelSerializer(ReferenceBaseSerializer):
    class Meta(ReferenceBaseSerializer.Meta):
        model = TransmissionModel


class DrivingAxleModelSerializer(ReferenceBaseSerializer):
    class Meta(ReferenceBaseSerializer.Meta):
        model = DrivingAxleModel


class SteeringAxleModelSerializer(ReferenceBaseSerializer):
    class Meta(ReferenceBaseSerializer.Meta):
        model = SteeringAxleModel
