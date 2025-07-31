from django.contrib import admin
from .models import Machine

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("factory_number", "machine_model", "engine_model", "shipment_date")
    search_fields = ("factory_number", "machine_model", "engine_model")
