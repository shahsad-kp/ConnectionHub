from django.test import TestCase, Client
from django.urls import reverse

from MainUsers.models import User


class LoginedClient(TestCase):
    def setUp(self) -> None:
        self.username = 'admin'
        self.password = 'admin'
        self.user = User.objects.create_superuser(
            username=self.username,
            password=self.password
        )
        self.client = Client()
        self.client.login(
            username=self.username,
            password=self.password
        )


class AdminUserPageTest(LoginedClient):
    def setUp(self):
        super().setUp()
        self.url = reverse('admin-users')

    def test_admin_users_page(self):
        response = self.client.get(self.url)
        self.assertEqual(
            first=response.status_code,
            second=200
        )
        self.assertTemplateUsed(response, 'admin-users.html')
        self.assertIn('users', response.context)


class AdminSearchUsersTest(LoginedClient):
    def setUp(self):
        super().setUp()
        self.url = reverse('admin-search-users')

    def test_success_users(self):
        response = self.client.get(self.url, data={'q': 'admin'})
        self.assertEqual(
            first=response.status_code,
            second=200
        )
        self.assertIn('results', response.json())
        self.assertIn('number_of_results', response.json())

    def test_invalid_data(self):
        response = self.client.get(self.url)
        self.assertEqual(
            first=response.status_code,
            second=401
        )
        self.assertIn('error', response.json())


class AdminProfilePagesTest(LoginedClient):
    def setUp(self):
        super().setUp()
        self.url = reverse(
            viewname='admin-profile-pages',
            args=[
                self.username
            ]
        )

    def test_admin_profile_pages(self):
        response = self.client.get(self.url)
        self.assertEqual(
            first=response.status_code,
            second=200
        )
        self.assertTemplateUsed(response, 'admin-profile-page.html')
        self.assertIn('username', response.context)
        self.assertIn('fullname', response.context)
        self.assertIn('profile_picture', response.context)
        self.assertIn('bio', response.context)
        self.assertIn('posts', response.context)
        self.assertIn('email', response.context)
        self.assertIn('phone_number', response.context)
        self.assertIn('number_of_followers', response.context)
        self.assertIn('number_of_followings', response.context)

    def test_invalid_username(self):
        url = reverse(
            viewname='admin-profile-pages',
            args=[
                'invalid_username'
            ]
        )
        response = self.client.get(url)
        self.assertEqual(
            first=response.status_code,
            second=404
        )


class AdminProfileDeleteTest(LoginedClient):
    def setUp(self):
        super().setUp()
        self.url = reverse(
            viewname='admin-profile-delete',
            args=[
                self.username
            ]
        )

    def test_success_delete(self):
        response = self.client.get(self.url)
        self.assertEqual(
            first=response.status_code,
            second=302
        )
        self.assertEqual(
            first=User.objects.count(),
            second=0
        )

    def test_invalid_username(self):
        url = reverse(
            viewname='admin-profile-delete',
            args=[
                'invalid_username'
            ]
        )
        response = self.client.get(url)
        self.assertEqual(
            first=response.status_code,
            second=404
        )
