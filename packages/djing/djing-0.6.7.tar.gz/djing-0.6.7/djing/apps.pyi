from django.apps import AppConfig
from djing.inertia_application import InertiaApplication as InertiaApplication

class DjingConfig(AppConfig):
    default_auto_field: str
    name: str
    def ready(self) -> None: ...
