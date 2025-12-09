from django import forms
from django.core.exceptions import ValidationError

from .models import (
    MachineModel, EngineModel, TransmissionModel,
    DrivingAxleModel, SteeringAxleModel,
    MaintenanceType, MaintenanceOrganization,
    FailureNode, RecoveryMethod
)



class BaseReferenceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            cls = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (cls + " form__input reference-form__input").strip()

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()

        model = self._meta.model
        qs = model.objects.filter(name__iexact=name)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("Элемент с таким названием уже существует.")

        return name


class MachineModelForm(BaseReferenceForm):
    class Meta:
        model = MachineModel
        fields = ["name", "description"]


class EngineModelForm(BaseReferenceForm):
    class Meta:
        model = EngineModel
        fields = ["name", "description"]


class TransmissionModelForm(BaseReferenceForm):
    class Meta:
        model = TransmissionModel
        fields = ["name", "description"]


class DrivingAxleModelForm(BaseReferenceForm):
    class Meta:
        model = DrivingAxleModel
        fields = ["name", "description"]


class SteeringAxleModelForm(BaseReferenceForm):
    class Meta:
        model = SteeringAxleModel
        fields = ["name", "description"]


class MaintenanceTypeForm(BaseReferenceForm):
    class Meta:
        model = MaintenanceType
        fields = ["name", "description"]


class MaintenanceOrganizationForm(BaseReferenceForm):
    class Meta:
        model = MaintenanceOrganization
        fields = ["name", "description"]


class FailureNodeForm(BaseReferenceForm):
    class Meta:
        model = FailureNode
        fields = ["name", "description"]


class RecoveryMethodForm(BaseReferenceForm):
    class Meta:
        model = RecoveryMethod
        fields = ["name", "description"]


def get_reference_form(model_class):
    return {
        MachineModel: MachineModelForm,
        EngineModel: EngineModelForm,
        TransmissionModel: TransmissionModelForm,
        DrivingAxleModel: DrivingAxleModelForm,
        SteeringAxleModel: SteeringAxleModelForm,
        MaintenanceType: MaintenanceTypeForm,
        MaintenanceOrganization: MaintenanceOrganizationForm,
        FailureNode: FailureNodeForm,
        RecoveryMethod: RecoveryMethodForm,
    }.get(model_class)
