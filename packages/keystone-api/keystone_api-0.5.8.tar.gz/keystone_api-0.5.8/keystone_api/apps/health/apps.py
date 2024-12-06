"""Application level configuration and setup.

Application configuration objects are used to override Django's default
application setup.
"""

from django.apps import AppConfig

from health_check.plugins import plugin_dir


class MyAppConfig(AppConfig):
    name = 'apps.health'

    def ready(self) -> None:
        from .backends import SMTPHealthCheck
        plugin_dir.register(SMTPHealthCheck)
