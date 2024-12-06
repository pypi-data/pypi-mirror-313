"""Expose an ASGI callable as a module-level variable named `application`."""

from django.core.asgi import get_asgi_application

application = get_asgi_application()
