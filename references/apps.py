from django.apps import AppConfig


class ReferencesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'references'
    verbose_name = "Справочники"

    def ready(self):
        import references.signals