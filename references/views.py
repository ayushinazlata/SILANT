from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.paginator import Paginator
from django.urls import reverse

from .models import (
    MachineModel, EngineModel, TransmissionModel, DrivingAxleModel,
    SteeringAxleModel, MaintenanceType, MaintenanceOrganization,
    FailureNode, RecoveryMethod
)
from .forms import get_reference_form
from django.core.cache import cache



MODELS = {
    'machine-model': MachineModel,
    'engine-model': EngineModel,
    'transmission-model': TransmissionModel,
    'driving-axle': DrivingAxleModel,
    'steering-axle': SteeringAxleModel,
    'maintenance-type': MaintenanceType,
    'maintenance-org': MaintenanceOrganization,
    'failure-node': FailureNode,
    'recovery-method': RecoveryMethod,
}

VERBOSE_NAMES = {
    'machine-model': "Модели техники",
    'engine-model': "Модели двигателя",
    'transmission-model': "Модели трансмиссии",
    'driving-axle': "Модели ведущего моста",
    'steering-axle': "Модели управляемого моста",
    'maintenance-type': "Виды ТО",
    'maintenance-org': "Организации ТО",
    'failure-node': "Узлы отказа",
    'recovery-method': "Способы восстановления",
}



def is_manager(user):
    return user.is_authenticated and user.groups.filter(name="Менеджер").exists()


@login_required
def reference_all_view(request):

    if not is_manager(request.user):
        return render(request, "errors/403.html", status=403)

    tab = request.GET.get("tab", "machine-model")
    page_number = request.GET.get("page", 1)
    search_query = request.GET.get("search", "").strip()

    if tab not in MODELS:
        raise Http404("Справочник не найден")

    model = MODELS[tab]

    form_errors = {}
    open_modal_id = None
    list_items = []

    cache_key = f"{model.__name__}_all_sorted"
    queryset = cache.get(cache_key)

    if queryset is None:
        queryset = model.objects.all().order_by("name")
        cache.set(cache_key, queryset, timeout=60 * 60)

    if search_query:
        queryset = queryset.filter(name__icontains=search_query)

    if request.method == "POST":
        if not is_manager(request.user):
            return render(request, "errors/403.html", status=403)

        pk = request.POST.get("edit_id")
        obj = get_object_or_404(model, pk=pk)

        FormClass = get_reference_form(model)
        form = FormClass(request.POST, instance=obj)

        if form.is_valid():
            form.save()
            return redirect(
                reverse("reference-all") +
                f"?tab={tab}&page={page_number}&search={search_query}"
            )
        else:
            form_errors[str(pk)] = form.errors
            open_modal_id = str(pk)

    paginator = Paginator(queryset, 10)
    page_obj = paginator.get_page(page_number)

    for item in page_obj:
        FormClass = get_reference_form(model)

        if open_modal_id == str(item.pk):
            form = FormClass(request.POST, instance=item)
        else:
            form = FormClass(instance=item)

        list_items.append({
            "item": item,
            "form": form
        })

    return render(request, "references/reference_all.html", {
        "tab": tab,
        "page_obj": page_obj,
        "page_items": list_items,
        "verbose_names": VERBOSE_NAMES,
        "is_manager": True,
        "open_modal_id": open_modal_id,
        "search_query": search_query,
    })


@login_required
def reference_create(request, model_name):

    if not is_manager(request.user):
        return render(request, "errors/403.html", status=403)

    if model_name not in MODELS:
        raise Http404("Справочник не найден")

    model = MODELS[model_name]
    FormClass = get_reference_form(model)

    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("reference-all") + f"?tab={model_name}")
    else:
        form = FormClass()

    return render(request, "references/reference_create.html", {
        "form": form,
        "model_name": model_name,
        "title": VERBOSE_NAMES.get(model_name, "Создание"),
    })


@login_required
def reference_detail(request, model_name, pk):

    if model_name not in MODELS:
        raise Http404("Справочник не найден")

    model = MODELS[model_name]
    obj = get_object_or_404(model, pk=pk)
    FormClass = get_reference_form(model)

    user = request.user
    manager = is_manager(user)

    open_modal_id = None

    if request.method == "POST":
        if not manager:
            return render(request, "errors/403.html", status=403)

        form = FormClass(request.POST, instance=obj)

        if form.is_valid():
            form.save()
            return redirect(reverse("reference-all") + f"?tab={model_name}")
        else:
            open_modal_id = str(obj.pk)
    else:
        form = FormClass(instance=obj)

    return render(request, "references/reference_detail.html", {
        "reference": obj,
        "form": form,
        "is_manager": manager,
        "open_modal_id": open_modal_id,
        "model_name": model_name,
    })
