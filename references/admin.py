from django.contrib import admin
from .models import (
    MachineModel, EngineModel, TransmissionModel,
    DrivingAxleModel, SteeringAxleModel,
    MaintenanceType, MaintenanceOrganization,
    FailureNode, RecoveryMethod
)


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(MachineModel, ReferenceAdmin)
admin.site.register(EngineModel, ReferenceAdmin)
admin.site.register(TransmissionModel, ReferenceAdmin)
admin.site.register(DrivingAxleModel, ReferenceAdmin)
admin.site.register(SteeringAxleModel, ReferenceAdmin)
admin.site.register(MaintenanceType, ReferenceAdmin)
admin.site.register(MaintenanceOrganization, ReferenceAdmin)
admin.site.register(FailureNode, ReferenceAdmin)
admin.site.register(RecoveryMethod, ReferenceAdmin)
