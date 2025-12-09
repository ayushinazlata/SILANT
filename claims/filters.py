import django_filters
from .models import Claim
from references.models import FailureNode, RecoveryMethod
from django.contrib.auth import get_user_model
from django import forms


User = get_user_model()

class ClaimFilter(django_filters.FilterSet):
    failure_node = django_filters.ModelChoiceFilter(
        queryset=FailureNode.objects.none(),
        label="Узел отказа"
    )
    recovery_method = django_filters.ModelChoiceFilter(
        queryset=RecoveryMethod.objects.none(),
        label="Способ восстановления"
    )
    service_company = django_filters.ModelChoiceFilter(
        field_name='service_company',
        queryset=User.objects.none(),
        label="Сервисная организация"
    )

    class Meta:
        model = Claim
        fields = ['failure_node', 'recovery_method', 'service_company']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        qs = self.queryset

        self.filters['failure_node'].queryset = FailureNode.objects.filter(
            id__in=qs.values_list('failure_node', flat=True)
        ).order_by("name")

        self.filters['recovery_method'].queryset = RecoveryMethod.objects.filter(
            id__in=qs.values_list('recovery_method', flat=True)
        ).order_by("name")

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
