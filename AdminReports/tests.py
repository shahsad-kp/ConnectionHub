from django.test import TestCase
from django.urls import reverse

from AdminReports.models import Report
from MainUsers.models import User


class LoginedUser(TestCase):
    def setUp(self):
        self.username = 'admin'
        self.password = 'admin'
        self.user = User.objects.create_superuser(
            username=self.username,
            password=self.password,
        )
        self.client.login(username='admin', password='admin')


class AdminReportsPageTest(LoginedUser):
    def setUp(self):
        super().setUp()
        self.url = reverse('admin_report_page')

    def test_admin_report_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_report_page.html')
        self.assertIn('reports', response.context)
        self.assertIn('number_of_reports', response.context)


class AdminReportHandledTest(LoginedUser):
    def setUp(self):
        super().setUp()
        self.report = self.user.reports_users.create(
            reported_user=self.user,
        )
        self.url = reverse('admin_report_handled', args=[1])

    def test_admin_report_handled(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(Report.objects.first().handled, True)

    def test_admin_report_handled_with_invalid_report_id(self):
        response = self.client.get(reverse('admin_report_handled', args=[999]))
        self.assertEqual(response.status_code, 404)