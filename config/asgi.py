import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import src.main.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kinoCMS.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            src.main.routing.websocket_urlpatterns
        )
    ),
})