from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from my_fake_api.handlers import WSRequestHandler


application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path("<uuid:api_id>/<path:path>", WSRequestHandler, name="ws_handler"),
    ]),
})
