"""
Application api handlers
"""
from rest_framework import routers, viewsets
from my_fake_api import models
from my_fake_api import serializers


class FakeAPIRequestLogViewSet(viewsets.ModelViewSet):
    """
    Get all user visible handler request log
    """
    serializer_class = serializers.FakeAPIRequestLogSerializer

    def get_queryset(self):
        """
        Provide access only to user visible handler logs.
        """
        groups = self.request.user.group_set.all()
        return models.APIRequest.objects.filter(request__group__in=groups)


router = routers.DefaultRouter()

router.register('logs', FakeAPIRequestLogViewSet, base_name="logs")
