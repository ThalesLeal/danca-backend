from django.apps import AppConfig


class ExampleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.example"
    label = "example"
    verbose_name = "Exemplo"
