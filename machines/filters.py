import django_filters
from .models import Machine
from references.models import (
    MachineModel, EngineModel, TransmissionModel,
    DrivingAxleModel, SteeringAxleModel
)



class MachineFilter(django_filters.FilterSet):
    machine_model = django_filters.ModelChoiceFilter(queryset=MachineModel.objects.none(), label="Модель техники")
    engine_model = django_filters.ModelChoiceFilter(queryset=EngineModel.objects.none(), label="Модель двигателя")
    transmission_model = django_filters.ModelChoiceFilter(queryset=TransmissionModel.objects.none(), label="Модель трансмиссии")
    driving_axle_model = django_filters.ModelChoiceFilter(queryset=DrivingAxleModel.objects.none(), label="Ведущий мост")
    steering_axle_model = django_filters.ModelChoiceFilter(queryset=SteeringAxleModel.objects.none(), label="Управляемый мост")

    class Meta:
        model = Machine
        fields = [
            'machine_model',
            'engine_model',
            'transmission_model',
            'driving_axle_model',
            'steering_axle_model',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        qs = self.queryset

        self.filters['machine_model'].queryset = MachineModel.objects.filter(
            id__in=qs.values_list('machine_model', flat=True)
        ).order_by("name")

        self.filters['engine_model'].queryset = EngineModel.objects.filter(
            id__in=qs.values_list('engine_model', flat=True)
        ).order_by("name")

        self.filters['transmission_model'].queryset = TransmissionModel.objects.filter(
            id__in=qs.values_list('transmission_model', flat=True)
        ).order_by("name")

        self.filters['driving_axle_model'].queryset = DrivingAxleModel.objects.filter(
            id__in=qs.values_list('driving_axle_model', flat=True)
        ).order_by("name")

        self.filters['steering_axle_model'].queryset = SteeringAxleModel.objects.filter(
            id__in=qs.values_list('steering_axle_model', flat=True)
        ).order_by("name")

        for field in self.form.fields.values():
            classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (classes + " select2").strip()
