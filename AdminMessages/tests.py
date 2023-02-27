from django.test import TestCase, Client
from django.urls import reverse

from MainUsers.models import User


class AdminMessagePageTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.username = 'admin'
        self.password = 'admin'
        self.user = User.objects.create_superuser(
            username=self.username,
            password=self.password
        )
        self.client.login(
            username=self.username,
            password=self.password
        )
        self.url = reverse(
            viewname='admin_messages_page'
        )

    def test_admin_messages_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='admin_messages_page.html'
        )

