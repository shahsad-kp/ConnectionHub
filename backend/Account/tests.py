from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from Account.models import User
from Account.views import CurrentUserView


class RegisterTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('register_view')
        self.username = 'shahsad-kp'
        self.username_1 = 'shahsadkp'
        self.email = 'm.shahsad@gmail.com'
        self.email_1 = 'shahsad.dev@gmail.com'
        self.password = 'admin@1234'
        self.phone = '+9100000000'
        self.phone_1 = '+911111111111'

    @property
    def data(self):
        return {
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'password': self.password,
            'confirm_password': self.password
        }

    def test_success(self):
        response = self.client.post(
            path=self.url,
            data=self.data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            'Status code not equal'
        )
        self.assertTrue(
            User.objects.filter(
                username=self.username
            ).first(),
            'User object not created'
        )
        user = User.objects.filter(
            username=self.username
        ).first()
        self.assertTrue(
            user.check_password(self.password),
            'Password is not equal'
        )

    def test_email_already_exists(self):
        User.objects.create_user(
            username=self.username_1,
            phone=self.phone_1,
            email=self.email,
            password=self.password
        )
        response = self.client.post(
            path=self.url,
            data=self.data
        )
        email_response = response.data.get('email')
        self.assertIsNotNone(email_response)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            'Status code is different'
        )

    def test_user_already_exists(self):
        User.objects.create_user(
            username=self.username,
            phone=self.phone_1,
            email=self.email_1,
            password=self.password
        )
        response = self.client.post(
            path=self.url,
            data=self.data
        )
        username_response = response.data.get('username')
        self.assertIsNotNone(username_response)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            'Status code is different'
        )

    def test_phone_already_exists(self):
        User.objects.create_user(
            username=self.username_1,
            phone=self.phone,
            email=self.email_1,
            password=self.password
        )
        response = self.client.post(
            path=self.url,
            data=self.data
        )
        username_response = response.data.get('phone')
        self.assertIsNotNone(username_response)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            'Status code is different'
        )


class CurrentAPITestCase(APITestCase):
    def setUp(self):
        self.email = 'user@email.com'
        self.username = 'Shahsad KP'
        self.phone = '+919999999999'
        self.password = 'admin@1234'
        self.user = User.objects.create_user(
            username=self.username,
            phone=self.phone,
            email=self.email,
            password=self.password
        )
        self.url = reverse('get_current_user')
        self.factory = APIRequestFactory()

    def test_get_current_user(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        view = CurrentUserView.as_view()
        response = view(request)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.data
        self.assertEqual(
            data.get('id'),
            str(self.user.id),
            'User id is not same'
        )
        self.assertEqual(
            data.get('username'),
            self.username,
            'Username is not same'
        )
        self.assertEqual(
            data.get('email'),
            self.email,
            'Email is not same'
        )
        self.assertEqual(
            data.get('phone'),
            self.phone,
            'Phone is not same'
        )
