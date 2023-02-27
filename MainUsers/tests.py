import json

from django.test import TestCase, Client
from django.urls import reverse

from AdminReports.models import Report
from .models import User, Follow


class HomeTest(TestCase):
    def setUp(self) -> None:
        self.username = 'username'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()

    def test_self_data(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse(
            viewname='profile-pages',
            args=[self.user.username]
        )
        response = self.client.get(
            path=url
        )
        self.assertTemplateUsed(response, 'profile-page.html')
        self.assertEqual(response.status_code, 200)


class SearchTest(TestCase):
    def setUp(self) -> None:
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.url = reverse('search-users')

    def test_without_data(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            path=self.url
        )
        self.assertEqual(response.status_code, 401)
        expected_data = {
            'error': 'Invalid parameter'
        }
        data = json.loads(response.content)
        self.assertDictEqual(data, expected_data)

    def test_default(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            path=self.url,
            data={'q': 'asw'}
        )
        data = json.loads(response.content)
        self.assertIn('results', data)
        self.assertIn('number_of_results', data)
        self.assertIsInstance(data['number_of_results'], int)
        self.assertIsInstance(data['results'], list)
        for item in data['results']:
            self.assertIsInstance(item, dict)
            self.assertIn('username', item)
            self.assertIn('fullname', item)
            self.assertIn('profile_url', item)
            self.assertIn('url', item)


class FollowTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.username_one = 'userone'
        self.password_one = 'passone'
        self.username_two = 'usertwo'
        self.password_two = 'passtwo'
        self.user_one = User.objects.create_user(username=self.username_one, password=self.password_one)
        self.user_two = User.objects.create_user(username=self.username_two, password=self.password_two)
        self.client.login(
            username=self.username_one,
            password=self.password_one
        )
        self.url = reverse(
            viewname='follow-user',
            args=[self.username_two]
        )

    def test_success(self):
        response = self.client.get(
            path=self.url
        )
        expected_data = {
            'success': True
        }
        data = json.loads(response.content)
        self.assertDictEqual(expected_data, data)
        self.assertEqual(response.status_code, 200)

    def test_failed(self):
        follow = Follow(follower=self.user_one, followee=self.user_two)
        follow.save()
        response = self.client.get(
            path=self.url
        )
        expected_data = {
            'success': False,
            'error': 'Already followed'
        }
        data = json.loads(response.content)
        self.assertDictEqual(expected_data, data)
        self.assertEqual(response.status_code, 400)


class UnfollowTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.username_one = 'userone'
        self.password_one = 'passone'
        self.username_two = 'usertwo'
        self.password_two = 'passtwo'
        self.user_one = User.objects.create_user(username=self.username_one, password=self.password_one)
        self.user_two = User.objects.create_user(username=self.username_two, password=self.password_two)
        self.client.login(
            username=self.username_one,
            password=self.password_one
        )
        self.url = reverse(
            viewname='unfollow-user',
            args=[self.username_two]
        )

    def test_success(self):
        follow = Follow(follower=self.user_one, followee=self.user_two)
        follow.save()
        response = self.client.get(
            path=self.url
        )
        expected_data = {
            'success': True
        }
        data = json.loads(response.content)
        self.assertDictEqual(expected_data, data)
        self.assertEqual(response.status_code, 200)

    def test_failed(self):
        response = self.client.get(
            path=self.url
        )
        expected_data = {
            'success': False,
            'error': 'Not followed'
        }
        data = json.loads(response.content)
        self.assertDictEqual(expected_data, data)
        self.assertEqual(response.status_code, 400)


class ReportTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.username_one = 'userone'
        self.password_one = 'passone'
        self.username_two = 'usertwo'
        self.password_two = 'passtwo'
        self.user_one = User.objects.create_user(username=self.username_one, password=self.password_one)
        self.user_two = User.objects.create_user(username=self.username_two, password=self.password_two)
        self.client.login(
            username=self.username_one,
            password=self.password_one
        )
        self.url = reverse(
            viewname='report-user',
            args=[self.username_two]
        )

    def test_success(self):
        response = self.client.get(self.url)
        expected_data = {
            'success': True
        }
        data = json.loads(response.content)
        self.assertDictEqual(expected_data, data)
        self.assertEqual(response.status_code, 200)

    def test_failed(self):
        report = Report(user=self.user_two, reported_user=self.user_one)
        report.save()
        response = self.client.get(self.url)
        data = json.loads(response.content)
        expected_data = {
            'error': 'Already reported'
        }
        self.assertDictEqual(data, expected_data)
        self.assertEqual(response.status_code, 409)
