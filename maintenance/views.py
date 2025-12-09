from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect

from .models import Maintenance
from machines.models import Machine
from .forms import MaintenanceForm


class MaintenanceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'forms/maintenance_form.html'

    def test_func(self):
        user = self.request.user
        return (
            user.groups.filter(name="Менеджер").exists()
            or user.groups.filter(name__in=["Клиент", "Сервисная организация"]).exists()
        )

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("У вас нет прав для создания ТО.")
        return super().handle_no_permission()

    def get_machine(self):
        pk = self.kwargs.get("pk")
        if pk:
            return get_object_or_404(Machine, pk=pk)
        return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs.setdefault("initial", {})

        machine = self.get_machine()
        if machine:
            kwargs["initial"]["machine"] = machine

        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["machine"] = self.get_machine()
        return ctx
    
    def form_valid(self, form):
        user = self.request.user
        machine = self.get_machine() or form.cleaned_data.get("machine")

        if not machine:
            raise PermissionDenied("Машина не указана.")

        if user.groups.filter(name="Клиент").exists():
            if machine.client != user:
                raise PermissionDenied("Вы можете добавлять ТО только к своим машинам.")

        if user.groups.filter(name="Сервисная организация").exists():
            if machine.service_company != user:
                raise PermissionDenied("Эта машина обслуживается другой сервисной компании.")

        form.instance.machine = machine
        form.instance.service_company = machine.service_company

        form.save()

        return redirect(reverse("home") + "?tab=maintenance")
