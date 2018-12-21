import factory
from my_fake_api import models
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    """
    Django user model factory
    """
    username = "api_user"

    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)


class APIFactory(factory.django.DjangoModelFactory):
    """
    Factory for `my_fake_api.models.API`
    """
    class Meta(object):
        """
        Modefactory meta settings
        """
        model = models.API

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.users.add(user)


class APIHandlerFactory(factory.django.DjangoModelFactory):
    """
    Factory for `my_fake_api.models.APIHandler`
    """
    api = factory.SubFactory(APIFactory)

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
