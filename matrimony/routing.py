from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import core.urls

application = ProtocolTypeRouter(
    {"websocket": AuthMiddlewareStack(URLRouter(core.urls.websocket_urlpatterns))}
)
