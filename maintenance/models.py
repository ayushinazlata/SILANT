from django.db import models
from django.conf import settings
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
    service_company = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'groups__name': 'Сервисная организация'},
        verbose_name="Сервисная организация"
    )

    class Meta:
        verbose_name = "ТО"
        verbose_name_plural = "ТО"
        ordering = ['-maintenance_date']

    def __str__(self):
        return f"ТО {self.maintenance_type} для {self.machine}"
    
    def save(self, *args, **kwargs):
        if self.machine and self.service_company != self.machine.service_company:
            self.service_company = self.machine.service_company

        super().save(*args, **kwargs)
