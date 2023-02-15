from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.apps.order"

    def ready(self) -> None:
        from . import signals
