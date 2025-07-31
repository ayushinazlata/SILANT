from django.db import models
from machines.models import Machine
from references.models import FailureNode, RecoveryMethod

class Claim(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name="Машина")
    failure_date = models.DateField(verbose_name="Дата отказа")
    operating_time = models.PositiveIntegerField(verbose_name="Наработка, м/час")
    failure_node = models.ForeignKey(FailureNode, on_delete=models.SET_NULL, null=True, verbose_name="Узел отказа")
    failure_description = models.TextField(verbose_name="Описание отказа")
    recovery_method = models.ForeignKey(RecoveryMethod, on_delete=models.SET_NULL, null=True, verbose_name="Способ восстановления")
    spare_parts_used = models.TextField(blank=True, verbose_name="Используемые запасные части")
    repair_date = models.DateField(verbose_name="Дата восстановления")
    downtime = models.PositiveIntegerField(editable=False, verbose_name="Время простоя техники")

    class Meta:
        verbose_name = "Рекламация"
        verbose_name_plural = "Рекламации"

    def save(self, *args, **kwargs):
        if self.failure_date and self.repair_date:
            self.downtime = (self.repair_date - self.failure_date).days
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Рекламация {self.machine.factory_number} ({self.failure_date})"
