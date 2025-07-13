"""
ASGI config for hexchess project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import apps.game.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hexchess.settings")
django.setup()

application = ProtocolTypeRouter(
    {
        # traditional http such as AJAX and GET requests
        "http": get_asgi_application(),
        # Websocket connections
        "websocket": AuthMiddlewareStack(
            URLRouter(apps.game.routing.websocket_urlpatterns)
        ),
    }
)
