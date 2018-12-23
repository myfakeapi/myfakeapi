from rest_framework.test import APITestCase, APIClient
from my_fake_api.tests import factories
from my_fake_api import models
from django.utils.crypto import get_random_string


class APIViewSetTestCase(APITestCase):
    """
    Testing `my_fake_api.api.views.APIViewSet`
    """

    api_url = "/api/apis/"

    def setUp(self):
        self.client = APIClient()

        self.username = get_random_string()
        self.user1 = factories.UserFactory(username=self.username)
        self.password = get_random_string()
        self.user1.set_password(self.password)

        self.user2 = factories.UserFactory()

        self.api1 = factories.APIFactory()
        self.api1.users.add(self.user1)

        self.api2 = factories.APIFactory()
        self.api2.users.add(self.user2)

    def _login(self):
        self.client.force_authenticate(user=self.user1)

    def test_non_authenticated_listing(self):
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, 403)

    def test_listing(self):
        self._login()
        response = self.client.get(self.api_url)
        response_item = response.json()[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response_item["id"], str(self.api1.pk))

    def test_non_authenticated_creation(self):
        response = self.client.get(self.api_url, data={
            "title": get_random_string()
        })
        self.assertEqual(response.status_code, 403)

    def test_creation(self):
        title = get_random_string()
        self._login()
        response = self.client.post(self.api_url, data={
            "title": title
        })
        self.assertEqual(response.status_code, 201)
        remote_pk = response.json()["id"]
        remote_obj = models.API.objects.filter(pk=remote_pk)
        self.assertTrue(remote_obj.exists())
        self.assertEqual(title, remote_obj.first().title)
        self.assertIn(self.user1, remote_obj.first().users.all())

    def test_non_authenticated_updating(self):
        response = self.client.patch("{}{}/".format(self.api_url, self.api1.pk), data={
            "title": get_random_string()
        })
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_updating(self):
        title = get_random_string()
        self._login()
        response = self.client.patch("{}{}/".format(self.api_url, self.api2.pk), data={
            "title": title
        })
        self.assertEqual(response.status_code, 404)

    def test_updating(self):
        title = get_random_string()
        self._login()
        response = self.client.patch("{}{}/".format(self.api_url, self.api1.pk), data={
            "title": title
        })
        self.assertEqual(response.status_code, 200)
        remote_pk = response.json()["id"]
        remote_obj = models.API.objects.filter(pk=remote_pk)
        self.assertTrue(remote_obj.exists())
        self.assertEqual(title, remote_obj.first().title)
        self.assertIn(self.user1, remote_obj.first().users.all())

    def test_non_authenticated_deletion(self):
        response = self.client.delete("{}{}/".format(self.api_url, self.api1.pk))
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_deletion(self):
        self._login()
        response = self.client.delete("{}{}/".format(self.api_url, self.api2.pk))
        self.assertEqual(response.status_code, 404)
        remote_obj = models.API.objects.filter(pk=self.api1.pk)
        self.assertTrue(remote_obj.exists())

    def test_deletion(self):
        self._login()
        response = self.client.delete("{}{}/".format(self.api_url, self.api1.pk))
        self.assertEqual(response.status_code, 204)
        remote_obj = models.API.objects.filter(pk=self.api1.pk)
        self.assertFalse(remote_obj.exists())
