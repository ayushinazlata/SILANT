from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from machines.models import Machine



User = get_user_model()


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = "__all__"
        widgets = {
            "shipment_date": forms.DateInput(attrs={"type": "date", "class": "form__input"}),

            "factory_number": forms.TextInput(attrs={
                "placeholder": "Укажите заводской номер машины",
                "class": "form__input"
            }),
            "engine_number": forms.TextInput(attrs={
                "placeholder": "Укажите заводской номер двигателя",
                "class": "form__input"
            }),
            "transmission_number": forms.TextInput(attrs={
                "placeholder": "Укажите заводской номер трансмиссии",
                "class": "form__input"
            }),
            "driving_axle_number": forms.TextInput(attrs={
                "placeholder": "Укажите заводской номер ведущего моста",
                "class": "form__input"
            }),
            "steering_axle_number": forms.TextInput(attrs={
                "placeholder": "Укажите заводской номер управляемого моста",
                "class": "form__input"
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["client"].queryset = User.objects.filter(groups__name="Клиент")
        self.fields["service_company"].queryset = User.objects.filter(groups__name="Сервисная организация")

        for field in self.fields.values():
            cls = field.widget.attrs.get("class", "")
            if "form__input" not in cls:
                field.widget.attrs["class"] = (cls + " form__input").strip()

    def clean_factory_number(self):
        number = self.cleaned_data.get("factory_number")

        if not number:
            raise ValidationError("Заводской номер обязателен.")

        existing = Machine.objects.filter(factory_number=number)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise ValidationError("Машина с таким заводским номером уже существует.")

        return number

    def clean_shipment_date(self):
        date_value = self.cleaned_data.get("shipment_date")
        if date_value and date_value > timezone.now().date():
            raise ValidationError("Дата отгрузки не может быть из будущего.")
        return date_value

    def clean(self):
        cleaned = super().clean()

        client = cleaned.get("client")
        service_company = cleaned.get("service_company")

        if client and not client.groups.filter(name="Клиент").exists():
            raise ValidationError("Выбранный пользователь не является Клиентом.")

        if service_company and not service_company.groups.filter(name="Сервисная организация").exists():
            raise ValidationError("Выбранный пользователь не является Сервисной компанией.")

        if self.user and not self.user.groups.filter(name="Менеджер").exists():
            raise ValidationError("Создавать машины может только менеджер.")

        return cleaned
