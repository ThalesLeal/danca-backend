from django.apps import AppConfig


class DefaultConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.auth"
    label = "appauth"

    def ready(self):
        from . import signals
