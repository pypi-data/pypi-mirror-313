from django.apps import AppConfig

from . import __version__


class AlumniConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "alumni"
    label = "alumni"
    verbose_name = f"AA Alumni v{__version__}"
