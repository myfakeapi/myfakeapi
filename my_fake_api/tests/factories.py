import factory
from my_fake_api import models


class APIHandlerFactory(factory.django.DjangoModelFactory):
    """
    Factory for `my_fake_api.models.APIHandler`
    """
    class Meta(object):
        """
        Modefactory meta settings
        """
        model = models.APIHandler


class APIRequestFactory(factory.django.DjangoModelFactory):
    """
    Factory for `my_fake_api.models.APIRequest`
    """
    api_handler = factory.SubFactory(APIHandlerFactory)

    class Meta(object):
        """
        Modelfactory meta settings
        """
        model = models.APIRequest
