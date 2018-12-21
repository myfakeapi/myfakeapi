from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from my_fake_api.tests import factories

import uuid


class HTTPHandlerTestCase(TestCase):
    """
    Testing `my_fake_api.handlers.http_request_handler`
    """
    def setUp(self):
        self.client = Client()
        self.path = "{}.php".format(get_random_string())
        self.response_code = 404
        self.response_content = get_random_string()

    def test(self):
        handler = factories.APIHandlerFactory(
            request_path=self.path,
            response_status_code=self.response_code,
            response_body=self.response_content,
        )
        with self.subTest("Should return preconfigured handler response"):
            url = reverse_lazy("my_fake_api:http_handler", kwargs={
                "api_id": handler.api.pk,
                "path": self.path
            })
            response = self.client.get(path=url)
            self.assertEqual(response.status_code, self.response_code)
            self.assertEqual(response.content, bytes(self.response_content, encoding="ascii"))

        with self.subTest("Should return error msg for malformatted group id"):
            url = reverse_lazy("my_fake_api:http_handler", kwargs={
                "api_id": uuid.uuid4(),
                "path": self.path
            })
            response = self.client.get(path=url)
            self.assertEqual(response.status_code, 404)
            self.assertIn(bytes("API Not Found", encoding="ascii"), response.content)

        with self.subTest("Should return error msg for malformatted path"):
            url = reverse_lazy("my_fake_api:http_handler", kwargs={
                "api_id": handler.api.pk,
                "path": "prefix_{}".format(self.path)
            })
            response = self.client.get(path=url)
            self.assertEqual(response.status_code, 404)
            self.assertIn(bytes("API Endpoint Not Found", encoding="ascii"), response.content)
