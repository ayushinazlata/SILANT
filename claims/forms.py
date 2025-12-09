from django import forms
from django.core.exceptions import ValidationError
from .models import Claim
from machines.models import Machine
from datetime import date



class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = "__all__"

        widgets = {
            "failure_date": forms.DateInput(attrs={"type": "date", "class": "form__input"}),
            "repair_date": forms.DateInput(attrs={"type": "date", "class": "form__input"}),
            "operating_time": forms.NumberInput(attrs={
                "placeholder": "Введите наработку, м/ч",
                "class": "form__input"
            }),
            "failure_description": forms.Textarea(attrs={
                "placeholder": "Опишите, что произошло...",
                "class": "form__textarea",
            }),
            "spare_parts_used": forms.Textarea(attrs={
                "placeholder": "Перечислите использованные запчасти...",
                "class": "form__textarea",
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            if self.user.groups.filter(name="Клиент").exists():
                self.fields["machine"].queryset = Machine.objects.filter(client=self.user)
            elif self.user.groups.filter(name="Сервисная организация").exists():
                self.fields["machine"].queryset = Machine.objects.filter(service_company=self.user)
            else:
                self.fields["machine"].queryset = Machine.objects.all()

        if "machine" in self.fields and self.initial.get("machine"):
            self.fields["machine"].widget = forms.HiddenInput()

        sc_field = self.fields.get("service_company")
        if sc_field:
            sc_field.required = False
            sc_field.widget = forms.HiddenInput()

            machine = None

            if "machine" in self.data:
                try:
                    machine = Machine.objects.get(pk=int(self.data["machine"]))
                except Exception:
                    pass
            elif self.instance.pk and self.instance.machine:
                machine = self.instance.machine
            elif isinstance(self.initial.get("machine"), Machine):
                machine = self.initial["machine"]

            if machine:
                sc_field.initial = machine.service_company

    def clean_operating_time(self):
        value = self.cleaned_data.get("operating_time")
        if value is not None and value < 0:
            raise ValidationError("Наработка не может быть отрицательной.")
        return value

    def clean(self):
        cleaned = super().clean()

        machine = cleaned.get("machine")
        failure_date = cleaned.get("failure_date")
        repair_date = cleaned.get("repair_date")

        if self.user and machine:
            if self.user.groups.filter(name="Клиент").exists():
                raise ValidationError("Клиенты не могут создавать рекламации.")

            if self.user.groups.filter(name="Сервисная организация").exists():
                if machine.service_company != self.user:
                    raise ValidationError("Вы можете добавлять рекламации только по машинам своей компании.")

        if failure_date and failure_date > date.today():
            raise ValidationError("Дата отказа не может быть из будущего.")

        if repair_date and repair_date > date.today():
            raise ValidationError("Дата восстановления не может быть из будущего.")

        if failure_date and repair_date and repair_date < failure_date:
            raise ValidationError("Дата восстановления не может быть раньше даты отказа.")

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)

        if instance.machine:
            instance.service_company = instance.machine.service_company

        if commit:
            instance.save()

        return instance
