"""
Application api handlers
"""
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import viewsets

from my_fake_api import models
from my_fake_api.api import serializers


class _BaseViewSet(viewsets.ModelViewSet):
    """
    Common features
    """
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)


class APIViewSet(_BaseViewSet):
    """
    ModelViewsSet for `my_fake_api.models.API`
    """
    model = models.API
    serializer_class = serializers.APISerializer

    def get_queryset(self):
        """
        Provide access only to user visible API objects.
        """
        return self.model.objects.filter(users__in=[self.request.user])

    def perform_create(self, serializer):
        """
        Store authenticated user as creator
        """
        obj = serializer.save()
        obj.users.add(self.request.user)


class APIHandlerViewSet(_BaseViewSet):
    """
    ModelViewsSet for `my_fake_api.models.APIHandler`
    """
    model = models.APIHandler
    serializer_class = serializers.APIHandlerSerializer

    def get_queryset(self):
        """
        Provide access only to handlers only from user visible API objects.
        """
        return self.model.objects.filter(api__in=self.request.user.api_set.all())


class APIRequestViewSet(_BaseViewSet):
    """
    ModelViewsSet for `my_fake_api.models.APIRequest`
    """
    model = models.APIRequest
    serializer_class = serializers.APIRequestSerializer

    def create(self, *args, **kwargs):
        """
        Logs should be created only by API requests
        """
        return super().list(self, *args, **kwargs)

    def get_queryset(self):
        """
        Provide access only to user visible handler logs.
        """
        return self.model.objects.filter(api_handler__api__in=self.request.user.api_set.all())
