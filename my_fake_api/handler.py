import re

from django import http
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt

from my_fake_api import models


@csrf_exempt
def mocker_request_handler(request, *args, **kwargs):

    group_id = kwargs.get("group_id")

    mocked_path = "/{}".format(kwargs.get("mocked_path", ""))
    mocked_path = mocked_path.replace("'", "")
    mocked_path = mocked_path.replace("\\", "")

    group = models.Group.objects.filter(pk=group_id).first()
    if not group:
        return http.HttpResponse("Group not found", status=404)

    for handler in group.item_set.filter(request_method=request.method):

        regex = re.sub("<([a-zA-Z0-9\-_]*)>", "([a-zA-Z0-9\-_]*)", handler.request_path)
        match = re.match(regex, mocked_path)

        if match:
            data = dict(
                zip(
                    re.findall("<([a-zA-Z0-9\-_]*)>", handler.request_path),
                    match.groups()
                )
            )

            template = Template(handler.response_body)
            context = Context(data)

            handler.log(request)
            return http.HttpResponse(template.render(context), status=handler.response_status_code)

    return http.HttpResponse("No predefined endpoint matched the request.", status=404)
