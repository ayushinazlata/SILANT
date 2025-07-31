from django.contrib import admin
from .models import Claim

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('machine', 'failure_date', 'failure_node', 'get_service_company', 'repair_date')
    list_filter = ('failure_node', 'recovery_method')
    readonly_fields = ('get_service_company',)

    def get_service_company(self, obj):
        return obj.machine.service_company
    get_service_company.short_description = "Сервисная компания"
