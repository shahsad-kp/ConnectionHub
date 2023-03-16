from django.urls import path

from . import consumer

websocket_urlpatterns = [
    path('chat/<str:username>/', consumer.ChatConsumer.as_asgi(), name='chat-consumer')
]
