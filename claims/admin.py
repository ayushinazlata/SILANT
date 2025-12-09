from django.contrib import admin
from .models import Claim
from .forms import ClaimForm


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    form = ClaimForm
    autocomplete_fields = ['machine', 'failure_node', 'recovery_method']
    ordering = ['machine']

    list_display = (
        'machine',
        'failure_date',
        'operating_time',
        'failure_node',
        'recovery_method',
        'repair_date',
        'downtime',
        'get_service_company',
    )

    list_filter = (
        'failure_node',
        'recovery_method',
        'failure_date',
        'machine__factory_number',
        'machine__service_company',
    )

    search_fields = (
        'machine__factory_number',
        'failure_description',
        'spare_parts_used',
    )

    readonly_fields = ('get_service_company', 'downtime',)

    def get_service_company(self, obj):
        return obj.machine.service_company
    get_service_company.short_description = "Сервисная компания"

    def add_view(self, request, form_url='', extra_context=None):
        response = super().add_view(request, form_url, extra_context)

        form = response.context_data.get('adminform').form if hasattr(response, 'context_data') else None

        if form and form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    self.message_user(request, f"Ошибка в поле '{field}': {error}", level='error')

        return response
