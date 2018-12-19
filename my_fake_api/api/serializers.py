from rest_framework import serializers
from my_fake_api import models


class FakeAPIHandlerSerializer(serializers.ModelSerializer):
    """
    Fake API handler serializer
    """
    class Meta:
        model = models.APIHandler
        fields = "__all__"


class APIRequestSerializer(serializers.ModelSerializer):
    """
    LogItem serializer
    """
    class Meta:
        model = models.APIRequest
        fields = "__all__"
