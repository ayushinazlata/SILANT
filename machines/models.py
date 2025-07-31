from django.db import models
from django.conf import settings
from references.models import (
    MachineModel, EngineModel, TransmissionModel,
    DrivingAxleModel, SteeringAxleModel
)

User = settings.AUTH_USER_MODEL

class Machine(models.Model):
    factory_number = models.CharField(max_length=100, unique=True, verbose_name="Зав. № машины")
    machine_model = models.ForeignKey(MachineModel, on_delete=models.SET_NULL, null=True, verbose_name="Модель техники")
    engine_model = models.ForeignKey(EngineModel, on_delete=models.SET_NULL, null=True, verbose_name="Модель двигателя")
    engine_number = models.CharField(max_length=100, verbose_name="Зав. № двигателя")
    transmission_model = models.ForeignKey(TransmissionModel, on_delete=models.SET_NULL, null=True, verbose_name="Модель трансмиссии")
    transmission_number = models.CharField(max_length=100, verbose_name="Зав. № трансмиссии")
    driving_axle_model = models.ForeignKey(DrivingAxleModel, on_delete=models.SET_NULL, null=True, verbose_name="Модель ведущего моста")
    driving_axle_number = models.CharField(max_length=100, verbose_name="Зав. № ведущего моста")
    steering_axle_model = models.ForeignKey(SteeringAxleModel, on_delete=models.SET_NULL, null=True, verbose_name="Модель управляемого моста")
    steering_axle_number = models.CharField(max_length=100, verbose_name="Зав. № управляемого моста")

    supply_contract = models.CharField(max_length=255, verbose_name="Договор поставки №, дата")
    shipment_date = models.DateField(verbose_name="Дата отгрузки с завода")
    consignee = models.CharField(max_length=255, verbose_name="Грузополучатель (конечный потребитель)")
    delivery_address = models.CharField(max_length=255, verbose_name="Адрес поставки (эксплуатации)")
    equipment = models.TextField(blank=True, verbose_name="Комплектация (доп. опции)")

    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="client_machines",
                               verbose_name="Клиент")
    service_company = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="service_machines",
                                        verbose_name="Сервисная компания")

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"

    def __str__(self):
        return f"{self.factory_number} ({self.machine_model})"
