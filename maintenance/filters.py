import django_filters
from .models import Maintenance
from references.models import MaintenanceType
from django.contrib.auth import get_user_model
from machines.models import Machine
from django import forms


User = get_user_model()

class MaintenanceFilter(django_filters.FilterSet):
    maintenance_type = django_filters.ModelChoiceFilter(queryset=MaintenanceType.objects.none(), label="Вид ТО")
    machine = django_filters.ModelChoiceFilter(queryset=Machine.objects.none(), label="Зав. № машины")
    service_company = django_filters.ModelChoiceFilter(
        field_name='service_company',
        queryset=User.objects.none(),
        label="Сервисная организация"
    )

    class Meta:
        model = Maintenance
        fields = ['maintenance_type', 'machine', 'service_company']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        qs = self.queryset

        self.filters['maintenance_type'].queryset = MaintenanceType.objects.filter(
            id__in=qs.values_list('maintenance_type', flat=True)
        ).order_by("name")

        self.filters['machine'].queryset = Machine.objects.filter(
            id__in=qs.values_list('machine', flat=True)
        ).order_by("factory_number")

        self.filters['service_company'].queryset = User.objects.filter(
            id__in=qs.values_list('service_company', flat=True),
            groups__name='Сервисная организация'
        ).order_by("username")

        # скрываем поле фильтра "Сервисная организация", если пользователь Сервисная организация
        if user and user.groups.filter(name="Сервисная организация").exists():
            field = self.form.fields["service_company"]
            field.widget = forms.HiddenInput()
            field.label = ""

        for field in self.form.fields.values():
            classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (classes + " select2").strip()
