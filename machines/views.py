from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Machine
from maintenance.models import Maintenance
from claims.models import Claim

from references.models import (
    MachineModel, EngineModel, TransmissionModel,
    DrivingAxleModel, SteeringAxleModel,
    MaintenanceType, FailureNode, RecoveryMethod
)

from .filters import MachineFilter
from maintenance.filters import MaintenanceFilter
from claims.filters import ClaimFilter
from .forms import MachineForm
from allauth.account.forms import LoginForm



def get_user_roles(user):
    return {
        "is_client": user.groups.filter(name="Клиент").exists(),
        "is_service": user.groups.filter(name="Сервисная организация").exists(),
        "is_manager": user.groups.filter(name="Менеджер").exists(),
    }


def machine_search_view(request):
    context = {}
    tab = request.GET.get('tab', 'machines')
    context['tab'] = tab

    if request.method == 'POST' and not request.user.is_authenticated:
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('/')
        else:
            context['form'] = form
            context['show_login'] = True
    else:
        context['form'] = LoginForm(request=request)

    if request.user.is_authenticated:
        user = request.user
        roles = get_user_roles(user)

        context.update(roles)

        if roles["is_client"]:
            machines = Machine.objects.filter(client=user)
        elif roles["is_service"]:
            machines = Machine.objects.filter(service_company=user)
        else:
            machines = Machine.objects.all()

        machines = machines.select_related(
            'machine_model', 'engine_model', 'transmission_model',
            'driving_axle_model', 'steering_axle_model',
            'client', 'service_company'
        )

        if tab == 'machines':
            machine_filter = MachineFilter(
                request.GET,
                queryset=machines.order_by('-shipment_date')
            )
            filtered = machine_filter.qs

            paginator = Paginator(filtered, 10)
            page_number = request.GET.get('page')
            context['machines'] = paginator.get_page(page_number)
            context['machine_filter'] = machine_filter

        elif tab == 'maintenance':
            maintenance_qs = Maintenance.objects.filter(
                machine__in=machines
            ).select_related(
                'maintenance_type', 'service_company', 'machine'
            ).order_by('-maintenance_date')

            maintenance_filter = MaintenanceFilter(
                request.GET,
                queryset=maintenance_qs,
                user=request.user
            )

            paginator = Paginator(maintenance_filter.qs, 20)
            page_number = request.GET.get('page')
            context['maintenances'] = paginator.get_page(page_number)
            context['maintenance_filter'] = maintenance_filter

        elif tab == 'claims':
            claim_qs = Claim.objects.filter(
                machine__in=machines
            ).select_related(
                'failure_node', 'recovery_method',
                'service_company', 'machine'
            ).order_by('-failure_date')

            claim_filter = ClaimFilter(
                request.GET,
                queryset=claim_qs,
                user=request.user
            )

            paginator = Paginator(claim_filter.qs, 20)
            page_number = request.GET.get('page')
            context['claims'] = paginator.get_page(page_number)
            context['claim_filter'] = claim_filter

        context['machine_models'] = MachineModel.objects.all()
        context['engine_models'] = EngineModel.objects.all()
        context['transmission_models'] = TransmissionModel.objects.all()
        context['driving_axle_models'] = DrivingAxleModel.objects.all()
        context['steering_axle_models'] = SteeringAxleModel.objects.all()

        context['maintenance_types'] = MaintenanceType.objects.all()
        context['failure_nodes'] = FailureNode.objects.all()
        context['recovery_methods'] = RecoveryMethod.objects.all()
        context['service_companies'] = get_user_model().objects.filter(
            groups__name='Сервисная организация'
        )
        context['maintenance_machines'] = machines

    factory_number = request.GET.get('factory_number')
    if factory_number and not request.user.is_authenticated:
        context['factory_number'] = factory_number
        try:
            context['machine'] = Machine.objects.get(factory_number=factory_number)
        except Machine.DoesNotExist:
            context['error'] = "Машина с таким заводским номером не найдена"

    return render(request, 'home/home.html', context)


class MachineDetailView(LoginRequiredMixin, DetailView):
    model = Machine
    template_name = "machines/machine_detail.html"
    context_object_name = "machine"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        roles = get_user_roles(user)
        obj = self.get_object()

        if roles["is_client"] and obj.client != user:
            raise PermissionDenied("У вас нет доступа к этой машине.")

        if roles["is_service"] and obj.service_company != user:
            raise PermissionDenied("У вас нет доступа к этой машине.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Machine.objects.select_related(
            'machine_model', 'engine_model', 'transmission_model',
            'driving_axle_model', 'steering_axle_model',
            'client', 'service_company'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        roles = get_user_roles(user)
        context.update(roles)

        machine = self.object
        tab = self.request.GET.get("tab", "maintenance")
        context["tab"] = tab

        if tab == "maintenance":
            qs = Maintenance.objects.filter(machine=machine).select_related(
                'maintenance_type', 'service_company'
            ).order_by('-maintenance_date')

            maintenance_filter = MaintenanceFilter(self.request.GET, queryset=qs, user=self.request.user)

            # Скрываем machine в фильтрах
            if 'machine' in maintenance_filter.form.fields:
                del maintenance_filter.form.fields['machine']

            context["maintenances"] = maintenance_filter.qs
            context["maintenance_filter"] = maintenance_filter

        elif tab == "claims":
            qs = Claim.objects.filter(machine=machine).select_related(
                'failure_node', 'recovery_method', 'service_company'
            ).order_by('-failure_date')

            claim_filter = ClaimFilter(self.request.GET, queryset=qs, user=self.request.user)

            context["claims"] = claim_filter.qs
            context["claim_filter"] = claim_filter

        return context


class MachineCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Machine
    form_class = MachineForm
    template_name = "forms/machine_form.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.request.user.groups.filter(name="Менеджер").exists()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Только менеджер может создавать машины.")
        return super().handle_no_permission()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if user.groups.filter(name="Клиент").exists():
            raise PermissionDenied("Клиенты не могут создавать машины.")

        if user.groups.filter(name="Сервисная организация").exists():
            raise PermissionDenied("Сервисные компании не могут создавать машины.")

        return super().dispatch(request, *args, **kwargs)
