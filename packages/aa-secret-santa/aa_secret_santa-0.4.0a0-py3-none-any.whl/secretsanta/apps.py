from django.apps import AppConfig

from . import __version__


class SecretSantaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "secretsanta"
    verbose_name = f'AA Secret Santa v{__version__}'
