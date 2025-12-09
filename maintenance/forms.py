from django import forms
from django.core.exceptions import ValidationError
from .models import Maintenance
from machines.models import Machine
from datetime import date
import re



class MaintenanceForm(forms.ModelForm):

    class Meta:
        model = Maintenance
        fields = "__all__" 
        widgets = {
            "order_number": forms.TextInput(attrs={
                "placeholder": "Введите номер заказ-наряда формата #2024-77КЕ23СИЛ",
                "class": "form__input"
            }),
            "maintenance_date": forms.DateInput(attrs={"type": "date", "class": "form__input"}),
            "order_date": forms.DateInput(attrs={"type": "date", "class": "form__input"}),
            "operating_time": forms.NumberInput(attrs={
                "placeholder": "Введите наработку, м/ч",
                "class": "form__input"
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            cls = field.widget.attrs.get("class", "")
            if "form__input" not in cls:
                field.widget.attrs["class"] = (cls + " form__input").strip()

        if self.user:
            if self.user.groups.filter(name="Клиент").exists():
                self.fields["machine"].queryset = Machine.objects.filter(client=self.user)

            elif self.user.groups.filter(name="Сервисная организация").exists():
                self.fields["machine"].queryset = Machine.objects.filter(service_company=self.user)

            else:
                self.fields["machine"].queryset = Machine.objects.all()

        # Если вызвали создание ТО со страницы машины - скрываем machine
        if "machine" in self.fields and self.initial.get("machine"):
            self.fields["machine"].widget = forms.HiddenInput()

        # Скрываем сервисную организацию
        sc_field = self.fields.get("service_company")
        if sc_field:
            sc_field.required = False
            sc_field.widget = forms.HiddenInput()

            machine = None

            if "machine" in self.data:
                try:
                    machine = Machine.objects.get(pk=int(self.data["machine"]))
                except:
                    pass

            elif self.instance.pk and self.instance.machine:
                machine = self.instance.machine

            elif isinstance(self.initial.get("machine"), Machine):
                machine = self.initial["machine"]

            elif isinstance(self.initial.get("machine"), int):
                try:
                    machine = Machine.objects.get(pk=self.initial["machine"])
                except:
                    pass

            if machine:
                sc_field.initial = machine.service_company

            
    def clean_operating_time(self):
        value = self.cleaned_data.get("operating_time")
        if value is not None and value < 0:
            raise ValidationError("Наработка не может быть отрицательной.")
        return value

    def clean_order_number(self):
        value = self.cleaned_data.get("order_number")

        pattern = r"^#\d{4}-\d{2}[A-Za-zА-Яа-я]{2}\d{2}СИЛ$"
        if not re.match(pattern, value):
            raise ValidationError("Номер заказ-наряда должен быть формата #2022-77КЕ23СИЛ")

        return value

    def clean(self):
        cleaned = super().clean()

        machine = cleaned.get("machine")
        maintenance_date = cleaned.get("maintenance_date")
        order_date = cleaned.get("order_date")
        operating_time = cleaned.get("operating_time")

        if not machine:
            raise ValidationError("Машина не указана.")

        if self.user and machine:
            if self.user.groups.filter(name="Клиент").exists():
                if machine.client != self.user:
                    raise ValidationError("Вы не можете добавлять ТО к чужой машине.")

            if self.user.groups.filter(name="Сервисная организация").exists():
                if machine.service_company != self.user:
                    raise ValidationError("Это машина другой сервисной компании.")

        if maintenance_date and maintenance_date > date.today():
            raise ValidationError("Дата ТО не может быть из будущего.")

        if order_date and order_date > date.today():
            raise ValidationError("Дата заказ-наряда не может быть из будущего.")

        if order_date and maintenance_date and order_date > maintenance_date:
            raise ValidationError("Дата заказ-наряда не может быть позже даты ТО.")

        if machine and operating_time is not None:
            last = Maintenance.objects.filter(machine=machine).order_by("-maintenance_date").first()
            if last and operating_time < last.operating_time:
                raise ValidationError(
                    f"Наработка не может быть меньше предыдущей ({last.operating_time} м/ч)."
                )

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)

        if instance.machine:
            instance.service_company = instance.machine.service_company

        if commit:
            instance.save()

        return instance
