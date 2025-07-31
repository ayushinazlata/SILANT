from django.db import models

# Базовый класс для всех справочников
class BaseReference(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

# Справочники для Машин
class MachineModel(BaseReference):
    class Meta:
        verbose_name = "Модель техники"
        verbose_name_plural = "Модели техники"

class EngineModel(BaseReference):
    class Meta:
        verbose_name = "Модель двигателя"
        verbose_name_plural = "Модели двигателя"

class TransmissionModel(BaseReference):
    class Meta:
        verbose_name = "Модель трансмиссии"
        verbose_name_plural = "Модели трансмиссии"

class DrivingAxleModel(BaseReference):
    class Meta:
        verbose_name = "Модель ведущего моста"
        verbose_name_plural = "Модели ведущего моста"

class SteeringAxleModel(BaseReference):
    class Meta:
        verbose_name = "Модель управляемого моста"
        verbose_name_plural = "Модели управляемого моста"

# Справочники для ТО и Рекламаций
class MaintenanceType(BaseReference):
    class Meta:
        verbose_name = "Вид ТО"
        verbose_name_plural = "Виды ТО"

class MaintenanceOrganization(BaseReference):
    class Meta:
        verbose_name = "Организация, проводившая ТО"
        verbose_name_plural = "Организации ТО"

class FailureNode(BaseReference):
    class Meta:
        verbose_name = "Узел отказа"
        verbose_name_plural = "Узлы отказа"

class RecoveryMethod(BaseReference):
    class Meta:
        verbose_name = "Способ восстановления"
        verbose_name_plural = "Способы восстановления"
