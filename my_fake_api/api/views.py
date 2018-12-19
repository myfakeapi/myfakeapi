"""
Application api handlers
"""
from rest_framework import viewsets

from my_fake_api import models
from my_fake_api.api import serializers


class APIRequestViewSet(viewsets.ModelViewSet):
    """
    Get all user visible handler request log
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
        return self.model.objects.filter(api_handlers__in=handlers)
