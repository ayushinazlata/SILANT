from django.contrib import admin
from .models import Maintenance
from .forms import MaintenanceForm


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    form = MaintenanceForm
    autocomplete_fields = ['machine', 'maintenance_type', 'organization']
    ordering = ['machine']

    fields = (
        'machine',
        'maintenance_type',
        'maintenance_date',
        'operating_time',
        'order_number',
        'order_date',
        'organization',
    )

    readonly_fields = ('get_service_company',)
    
    list_display = (
        'machine',
        'maintenance_type',
        'maintenance_date',
        'operating_time',
        'order_number',
        'order_date',
        'organization',
        'get_service_company',
    )

    list_filter = (
        'maintenance_type',
        'maintenance_date',
        'organization',
        'machine__machine_model',
        'machine__engine_model',
        'machine__transmission_model',
        'machine__driving_axle_model',
        'machine__steering_axle_model',
        'machine__factory_number',
        'machine__service_company',
    )

    search_fields = (
        'machine__factory_number',
        'order_number',
        'organization__name',
        'maintenance_type__name',
    )

    def get_service_company(self, obj):
        return obj.machine.service_company
    get_service_company.short_description = "Сервисная компания"
