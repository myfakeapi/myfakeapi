"""
Application model serializers
"""
from rest_framework import serializers
from my_fake_api import models


class APISerializer(serializers.ModelSerializer):
    """
    Serializer for `my_fake_api.models.API`
    """
    class Meta(object):
        """
        Serializer meta settings
        """
        model = models.API
        exclude = ["users"]


class APIHandlerSerializer(serializers.ModelSerializer):
    """
    Serializer for `my_fake_api.models.APIHandler`
    """
    class Meta(object):
        """
        Serializer meta settings
        """
        model = models.APIHandler
        fields = "__all__"


class APIRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for `my_fake_api.models.APIRequest`
    """
    class Meta(object):
        """
        Serializer meta settings
        """
        model = models.APIRequest
        fields = "__all__"
