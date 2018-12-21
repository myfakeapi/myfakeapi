import re

from django import http
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt

from my_fake_api import models


@csrf_exempt
def http_request_handler(request, *args, **kwargs):

    api_id = kwargs.get("api_id")

    path = kwargs.get("path", "")

    for char in ("'", "\\"):
        path = path.replace(char, "")

    api = models.API.objects.filter(pk=api_id).first()
    if not api:
        return http.HttpResponse("API Not Found", status=404)

    for handler in api.apihandler_set.filter(request_method=request.method):
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

            handler.log()
            return http.HttpResponse(template.render(context), status=handler.response_status_code)

    return http.HttpResponse("API Endpoint Not Found", status=404)
