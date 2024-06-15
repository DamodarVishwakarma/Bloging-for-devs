from django.apps import AppConfig
from .settings import CUSER_SETTINGS


class CoreConfig(AppConfig):
    name = 'core'
    default_auto_field = 'django.db.models.AutoField'
    verbose_name = CUSER_SETTINGS['app_verbose_name']

    def ready(self):
        import core.signals