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
        Provide access only to user visible API.
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
        Provide access only to user visible API handlers.
        """
        api_list = self.request.user.api_set.all()
        return self.model.objects.filter(api__in=api_list)


class APIRequestViewSet(_BaseViewSet):
    """
    ModelViewsSet for `my_fake_api.models.APIRequest`
    """
    model = models.APIRequest
    serializer_class = serializers.APIRequestSerializer

    def get_queryset(self):
        """
        Provide access only to user visible handler logs.
        """
        api_list = self.request.user.api_set.all()
        return self.model.objects.filter(api_handler__api__in=api_list)
