from django.apps import AppConfig


class ScientificmethodConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scientificmethod'

    def ready(self):
        import scientificmethod.signals
