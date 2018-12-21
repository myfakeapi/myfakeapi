"""
Application api handlers
"""
from rest_framework import viewsets

from my_fake_api import models
from my_fake_api.api import serializers


class APIViewSet(viewsets.ModelViewSet):
    """
    ModelViewsSet for `my_fake_api.models.API`
    """
    model = models.API
    serializer_class = serializers.APISerializer


class APIHandlerViewSet(viewsets.ModelViewSet):
    """
    ModelViewsSet for `my_fake_api.models.APIHandler`
    """
    model = models.APIHandler
    serializer_class = serializers.APIHandlerSerializer


class APIRequestViewSet(viewsets.ModelViewSet):
    """
    ModelViewsSet for `my_fake_api.models.APIRequest`
    """
    model = models.APIRequest
    serializer_class = serializers.APIRequestSerializer

    def get_queryset(self):
        """
        Provide access only to user visible handler logs.
        """
        if not self.request.user.is_authenticated:
            return self.model.objects.none()

        handlers = self.request.user.apihandler_set.all()
        return self.model.objects.filter(api_handler__in=handlers)
