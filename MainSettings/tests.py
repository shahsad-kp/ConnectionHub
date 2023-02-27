import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from MainUsers.models import User


class LoginedClient(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpass'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)


class HomeTest(LoginedClient):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse(
            viewname='settings-home'
        )

    def test_default(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response=response,
            expected_url=reverse('profile-settings')
        )


class UpdateProfileTest(LoginedClient):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('profile-settings')

    def test_get_page(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response=response,
            template_name='profile-update-settings.html'
        )

    def test_invalid_data(self):
        response = self.client.post(
            path=self.url,
            data={
                'username': 'error'
            }
        )
        self.assertEqual(response.status_code, 400)
        expected_data = {
            'error': 'Invalid data'
        }
        data = json.loads(response.content)
        self.assertDictEqual(expected_data, data)

    def test_duplicate_username(self):
        new_username = 'duplicateusername'
        User.objects.create_user(
            username=new_username,
            email='email@test.com',
            password='testpassword'
        )
        response = self.client.post(
            path=self.url,
            data={
                'username': new_username,
                'fullname': '',
                'email': '',
                'bio': '',
                'phone': ''
            }
        )
        self.assertEqual(response.status_code, 409)
        expected_data = {
            'error': 'Username is not available'
        }
        data = json.loads(response.content)
        self.assertDictEqual(expected_data, data)

    def test_duplicate_email(self):
        new_email = 'duplicate@password.com'
        User.objects.create_user(
            username='username',
            email=new_email,
            password='testpassword'
        )
        response = self.client.post(
            path=self.url,
            data={
                'username': '',
                'fullname': '',
                'email': new_email,
                'bio': '',
                'phone': ''
            }
        )
        self.assertEqual(response.status_code, 409)
        expected_data = {
            'error': 'Email is already connected to another account'
        }
        data = json.loads(response.content)
        self.assertDictEqual(expected_data, data)

    def test_update_username(self):
        data = {
            'username': 'newusername',
            'fullname': '',
            'email': '',
            'bio': '',
            'phone': '',
            'profile-picture': ''
        }
        self.client.post(
            path=self.url,
            data=data
        )
        User.objects.get(username=data['username'])

    def test_update_fullname(self):
        data = {
            'username': '',
            'fullname': 'newfullname',
            'email': '',
            'bio': '',
            'phone': '',
            'profile-picture': ''
        }
        self.client.post(
            path=self.url,
            data=data
        )
        user = User.objects.get(username=self.username)
        self.assertEqual(user.full_name, data['fullname'])

    def test_update_email(self):
        data = {
            'username': '',
            'fullname': '',
            'email': 'email@test.com',
            'bio': '',
            'phone': '',
            'profile-picture': ''
        }
        self.client.post(
            path=self.url,
            data=data
        )
        user = User.objects.get(username=self.username)
        self.assertEqual(user.email, data['email'])

    def test_update_bio(self):
        data = {
            'username': '',
            'fullname': '',
            'email': '',
            'bio': 'newbio',
            'phone': '',
            'profile-picture': ''
        }
        self.client.post(
            path=self.url,
            data=data
        )
        user = User.objects.get(username=self.username)
        self.assertEqual(user.bio, data['bio'])

    def test_update_phone(self):
        data = {
            'username': '',
            'fullname': '',
            'email': '',
            'bio': '',
            'phone': 'newphone',
            'profile-picture': ''
        }
        self.client.post(
            path=self.url,
            data=data
        )
        user = User.objects.get(username=self.username)
        self.assertEqual(user.phone_number, data['phone'])

    def test_update_profile_picture(self):
        data = {
            'username': '',
            'fullname': '',
            'email': '',
            'bio': '',
            'phone': '',
            'profile-picture': SimpleUploadedFile(
                name='test_image.jpg',
                content=open('test_files/profile_image_one.jpg', 'rb').read(),
                content_type='image/jpeg'
            )
        }
        self.client.post(
            path=self.url,
            data=data
        )
        user = User.objects.get(username=self.username)
        self.assertIsNotNone(user.profile_picture)

    def test_update_all(self):
        data = {
            'username': 'newusername',
            'fullname': 'newfullname',
            'email': 'test@email.com',
            'bio': 'newbio',
            'phone': 'newphone',
            'profile-picture': SimpleUploadedFile(
                name='test_image.jpg',
                content=open('test_files/profile_image_one.jpg', 'rb').read(),
                content_type='image/jpeg'
            )
        }
        self.client.post(
            path=self.url,
            data=data
        )
        user = User.objects.get(username=data['username'])
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.full_name, data['fullname'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.bio, data['bio'])
        self.assertEqual(user.phone_number, data['phone'])
        self.assertIsNotNone(user.profile_picture)


class PasswordUpdateTest(LoginedClient):
    def setUp(self):
        super().setUp()
        self.url = reverse('profile-password')

    def test_get_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='profile-change-password.html'
        )

    def test_invalid_data(self):
        response = self.client.post(
            path=self.url,
            data={
                'asdf': 'asdf',
            }
        )
        self.assertEqual(response.status_code, 400)
        expected_data = {
            'error': 'Invalid data'
        }
        data = json.loads(response.content)
        self.assertDictEqual(expected_data, data)

    def test_wrong_current_password(self):
        response = self.client.post(
            path=self.url,
            data={
                'old-password': 'wrongpassword',
                'new-password': 'newpassword',
            }
        )
        self.assertEqual(response.status_code, 403)
        expected_data = {
            'error': 'Old password is incorrect'
        }
        data = json.loads(response.content)
        self.assertDictEqual(expected_data, data)

    def test_update_password(self):
        new_password = 'newpassword'
        data = {
            'old-password': self.password,
            'new-password': new_password,
        }
        response = self.client.post(
            path=self.url,
            data=data
        )
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username=self.username)
        self.assertTrue(user.check_password(new_password))


class DeleteAccountTest(LoginedClient):
    def setUp(self):
        super().setUp()
        self.url = reverse('profile-delete')

    def test_get_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='profile-delete-account.html'
        )

    def test_invalid_data(self):
        response = self.client.post(
            path=self.url,
            data={
                'asdf': 'asdf',
            }
        )
        self.assertEqual(response.status_code, 400)
        expected_data = {
            'error': 'Invalid data'
        }
        data = json.loads(response.content)
        self.assertDictEqual(expected_data, data)

    def test_wrong_password(self):
        response = self.client.post(
            path=self.url,
            data={
                'password': 'wrongpassword',
            }
        )
        self.assertEqual(response.status_code, 403)
        expected_data = {
            'error': 'Password is incorrect'
        }
        data = json.loads(response.content)
        self.assertDictEqual(expected_data, data)

    def test_delete_account(self):
        data = {
            'password': self.password,
        }
        response = self.client.post(
            path=self.url,
            data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=self.username).exists())


class HelpMessageTest(LoginedClient):
    def setUp(self):
        super().setUp()
        self.url = reverse('settings-help')

    def test_get_page(self):
        response = self.client.get(
            path=self.url
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='help-center.html'
        )

    def test_invalid_data(self):
        response = self.client.post(
            path=self.url,
            data={
                'sf': 'sdf'
            }
        )
        self.assertEqual(response.status_code, 400)
        expected_data = {
            'error': 'Invalid data'
        }
        data = json.loads(response.content)
        self.assertDictEqual(data, expected_data)

    def test_valid_data(self):
        data = {
            'subject': 'test subject',
            'message': 'test message'
        }
        response = self.client.post(
            path=self.url,
            data=data
        )
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'success': True
        }
        data = json.loads(response.content)
        self.assertDictEqual(data, expected_data)
