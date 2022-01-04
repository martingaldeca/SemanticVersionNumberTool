from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # https://django-axes.readthedocs.io/en/latest/6_integration.html
        # This signal import is to DRF to work with Django Axes
        from core import signals  # noqa
