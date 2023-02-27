import json

from django.test import TestCase, Client
from django.urls import reverse

from MainUsers.models import User


class HomeTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_superuser(
            username=self.username,
            password=self.password
        )
        self.url = reverse(
            viewname='admin-home'
        )

    def test_without_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response=response,
            expected_url=reverse('admin-login')
        )

    def test_with_login(self):
        self.client.login(
            username=self.username,
            password=self.password
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin-home.html')


class LoginTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_superuser(
            username=self.username,
            password=self.password
        )
        self.url = reverse(
            viewname='admin-login'
        )

    def test_get_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin-login.html')

    def test_invalid_data(self):
        response = self.client.post(
            path=self.url,
            data={
                'invalid': 'invalid'
            }
        )
        self.assertEqual(response.status_code, 400)
        expected_data = {
            'error': 'Invalid data'
        }
        data = json.loads(response.content)
        self.assertDictEqual(expected_data, data)

    def test_invalid_cred(self):
        response = self.client.post(
            path=self.url,
            data={
                'username': self.username,
                'password': 'invalidcred'
            }
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        expected_data = {
            'error': 'Invalid username or password'
        }
        self.assertDictEqual(data, expected_data)

    def test_valid_cred(self):
        response = self.client.post(
            path=self.url,
            data={
                'username': self.username,
                'password': self.password
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response=response,
            expected_url=reverse(
                viewname='admin-home'
            )
        )


class AdminLogout(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_superuser(
            username=self.username,
            password=self.password
        )
        self.url = reverse(
            viewname='admin-logout'
        )

    def test_default(self):
        self.client.login(
            username=self.username,
            password=self.password
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response=response,
            expected_url=reverse('admin-login')
        )
