"""
ASGI config for ConnectionHub project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.layers import get_channel_layer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.core.asgi import get_asgi_application

import Communications.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ConnectionHub.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                Communications.routing.websocket_urlpatterns
            )
        ),
    }
)

application = ASGIStaticFilesHandler(application)

channel_layer = get_channel_layer()

