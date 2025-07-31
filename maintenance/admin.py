from django.contrib import admin
from .models import Maintenance

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('machine', 'maintenance_type', 'maintenance_date', 'get_service_company')
    list_filter = ('maintenance_type',)
    readonly_fields = ('get_service_company',)

    def get_service_company(self, obj):
        return obj.machine.service_company
    get_service_company.short_description = "Сервисная компания"
