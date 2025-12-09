from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Claim
from machines.models import Machine
from .forms import ClaimForm



class ClaimCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Claim
    form_class = ClaimForm
    template_name = "forms/claim_form.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        user = self.request.user

        if user.groups.filter(name="Менеджер").exists():
            return True

        if user.groups.filter(name="Сервисная организация").exists():
            return True

        return False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("У вас нет прав для создания рекламации.")
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
        machine = self.get_machine()

        if machine:
            form.instance.machine = machine

        if user.groups.filter(name="Менеджер").exists():
            form.instance.service_company = machine.service_company
            return super().form_valid(form)

        if user.groups.filter(name="Клиент").exists():
            raise PermissionDenied("Клиенты не могут добавлять рекламации.")

        if user.groups.filter(name="Сервисная организация").exists():
            if not machine or machine.service_company != user:
                raise PermissionDenied("Это машина другой сервисной компании.")

            form.instance.service_company = machine.service_company
            return super().form_valid(form)

        raise PermissionDenied("Недостаточно прав.")
