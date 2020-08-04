# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
	'websocket': AuthMiddlewareStack(
		URLRouter(
			chat.routing.websocket_urlpatterns
		)
	),
	# Empty for now (http->django views is added by default)
})