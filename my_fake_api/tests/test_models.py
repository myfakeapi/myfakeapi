from django.test import TestCase
from django.utils.crypto import get_random_string
from my_fake_api.tests import factories
from my_fake_api import models


class APITestCase(TestCase):
    """
    Testing `my_fake_api.models.API`
    """
    def setUp(self):
        self.api = factories.APIFactory()

    def test_str(self):
        """ Object string representation should include `title`"""
        title = get_random_string()
        self.api.title = title
        self.assertIn(title, str(self.api))


class APIHandlerTestCase(TestCase):
    """
    Testing `my_fake_api.models.APIHandlers`
    """
    def setUp(self):
        self.handler = factories.APIHandlerFactory()

    def test_str(self):
        """ Object string representation should include `request_path`"""
        request_path = get_random_string()
        self.handler.request_path = request_path
        self.assertIn(request_path, str(self.handler))

    def test_log(self):
        self.assertFalse(models.APIRequest.objects.exists())
        self.handler.log()
        self.assertEqual(models.APIRequest.objects.count(), 1)


class APIRequestTestCase(TestCase):
    """
    Testing `my_fake_api.models.APIHandlers`
    """
    def setUp(self):
        self.handler = factories.APIHandlerFactory()
        self.request = factories.APIRequestFactory(api_handler=self.handler)

    def test_str(self):
        """ Object string representation should include `request_path` and request date """
        request_path = get_random_string()
        self.request.request_path = request_path
        self.assertIn(request_path, str(self.request))
        self.assertIn(str(self.request.created.year), str(self.request))
