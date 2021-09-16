# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
import quickvote.routing

routing = [
    *chat.routing.websocket_urlpatterns,
    *quickvote.routing.websocket_urlpatterns
]

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing,
        )
    )
})
