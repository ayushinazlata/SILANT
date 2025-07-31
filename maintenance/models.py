from django.db import models
from machines.models import Machine
from references.models import MaintenanceType, MaintenanceOrganization

class Maintenance(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name="Машина")
    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.SET_NULL, null=True, verbose_name="Вид ТО")
    maintenance_date = models.DateField(verbose_name="Дата проведения ТО")
    operating_time = models.PositiveIntegerField(verbose_name="Наработка, м/час")
    order_number = models.CharField(max_length=100, verbose_name="№ заказ-наряда")
    order_date = models.DateField(verbose_name="Дата заказ-наряда")
    organization = models.ForeignKey(MaintenanceOrganization, on_delete=models.SET_NULL, null=True,
                                     verbose_name="Организация, проводившая ТО")

    class Meta:
        verbose_name = "ТО"
        verbose_name_plural = "ТО"

    def __str__(self):
        return f"ТО {self.maintenance_type} для {self.machine}"
