"""
ASGI config for chicoexchange project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler
from django.core.asgi import get_asgi_application
import store.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chicoexchange.settings')

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            store.routing.websocket_urlpatterns
        )
    ),
})
