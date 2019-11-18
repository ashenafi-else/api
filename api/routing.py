from channels.auth import AuthMiddlewareStack
from django.urls import path
from channels.routing import (
    ProtocolTypeRouter,
    URLRouter,
)
from . import consumers


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [path('ws/execute_operations/<uuid:session>', consumers.CallOperation)]
        )
    ),
})
