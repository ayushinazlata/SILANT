from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import (
    MachineModel, EngineModel, TransmissionModel,
    DrivingAxleModel, SteeringAxleModel,
    MaintenanceType, MaintenanceOrganization,
    FailureNode, RecoveryMethod
)

REFERENCE_MODELS = (
    MachineModel, EngineModel, TransmissionModel,
    DrivingAxleModel, SteeringAxleModel,
    MaintenanceType, MaintenanceOrganization,
    FailureNode, RecoveryMethod
)

@receiver([post_save, post_delete])
def clear_reference_cache(sender, **kwargs):
    if sender in REFERENCE_MODELS:
        cache_key = f"{sender.__name__}_all"
        cache.delete(cache_key)
