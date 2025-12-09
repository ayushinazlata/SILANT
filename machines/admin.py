from django.contrib import admin
from .models import Machine
from .forms import MachineForm



@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    form = MachineForm
    autocomplete_fields = [
        'client', 'service_company',
        'machine_model', 'engine_model', 'transmission_model',
        'driving_axle_model', 'steering_axle_model',
    ]
    ordering = ['factory_number']

    list_display = (
        "factory_number", "machine_model", "engine_model", "engine_number",
        "transmission_model", "transmission_number",
        "driving_axle_model", "driving_axle_number",
        "steering_axle_model", "steering_axle_number",
        "shipment_date", "client", "service_company",
    )

    search_fields = (
        "factory_number", 
        "engine_number", 
        "transmission_number",
        "driving_axle_number", 
        "steering_axle_number",
        "client__company_name", 
        "service_company__company_name",
        "machine_model__name",
        "engine_model__name",
        "transmission_model__name",
        "driving_axle_model__name",
        "steering_axle_model__name",
    )

    list_filter = ("machine_model", "engine_model", "transmission_model", "shipment_date")
    list_per_page = 50