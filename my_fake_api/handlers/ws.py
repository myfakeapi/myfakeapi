from channels.generic.websocket import WebsocketConsumer
from django.template import Template, Context
from my_fake_api import models
import re


class WSRequestHandler(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        kwargs = self.scope["url_route"]["kwargs"]
        api_id = kwargs.get("api_id")
        path = kwargs.get("path", "")

        for char in ("'", "\\"):
            path = path.replace(char, "")

        api = models.API.objects.filter(pk=api_id).first()
        if not api:
            self.send(text_data="API Not Found")
            return

        for handler in api.apihandler_set.filter(mock_type=models.WEBSOCKETS):
            regex = re.sub("<([a-zA-Z0-9-_]*)>", "([a-zA-Z0-9-_]*)", handler.request_path)
            match = re.match(regex, path)

            if match:
                data = dict(
                    zip(
                        re.findall("([a-zA-Z0-9-_]*)", handler.request_path),
                        match.groups()
                    )
                )

                template = Template(handler.response_body)
                context = Context(data)
                self.send(text_data=template.render(context))
                return

        self.send(text_data="API Endpoint Not Found")
        return
