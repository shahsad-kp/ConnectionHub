import json
from django.test import TestCase, Client
from django.urls import reverse

from MainUsers.models import User


class RegisterHomeTest(TestCase):
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password, email='testemail@gmail.com')
        self.client = Client()
        self.url = reverse('user-register')

    def test_register_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_register_post_no_data(self):
        response = self.client.post(
            self.url
        )
        data = json.loads(response.content)
        expected = {
            'error': 'Invalid data'
        }
        self.assertDictEqual(data, expected)

    def test_register_post_with_same_username(self):
        data = {
            'username': self.user.username,
            'password': 'password',
            'email': 'sdfsdf@dfsf.com',
            'fullname': 'fullname'
        }
        response = self.client.post(
            path=self.url,
            data=data
        )
        expected_data = {
            'error': 'Username already taken'
        }
        data = json.loads(response.content)
        self.assertDictEqual(data, expected_data)

    def test_register_post_with_same_email(self):
        data = {
            'username': 'username',
            'password': 'password',
            'email': self.user.email,
            'fullname': 'fullname'
        }
        response = self.client.post(
            path=self.url,
            data=data
        )
        expected_data={
            'error': 'Email already connected to an account'
        }
        data = json.loads(response.content)
        self.assertDictEqual(data, expected_data)

    def test_register_post_success(self):
        data = {
            'username': 'username',
            'password': 'password',
            'email': 'shahsdfsdf@gsd.com',
            'fullname': 'fullname'
        }
        response = self.client.post(
            path=self.url,
            data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user-home'), fetch_redirect_response=False)

    def test_register_redirect_if_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('user-home'))


class LoginHomeTest(TestCase):
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.url = reverse('user-login')

    def test_login_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_post_no_data(self):
        response = self.client.post(
            self.url
        )
        data = json.loads(response.content)
        expected = {
            'error': 'Invalid data'
        }
        self.assertDictEqual(
            data,
            expected
        )

    def test_login_success(self):
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertRedirects(response, reverse('user-home'))

    def test_login_failure(self):
        response = self.client.post(self.url, {'username': 'invaliduser', 'password': 'invalidpass'})
        data = json.loads(response.content)
        expected = {
            'error': 'Invalid username or password'
        }
        self.assertDictEqual(data, expected)

    def test_login_redirect_if_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('user-home'))


class HomeTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.url = reverse('user-home')

    def test_without_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('Location', response)
        self.assertEqual(response['Location'], reverse('user-login') + '?next=' + self.url)

    def test_with_login(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'user-home.html')


class LogoutTest(TestCase):
    def test_default(self):
        client = Client()
        url = reverse('user-logout')
        response = client.get(url)
        self.assertEqual(response.status_code, 302)