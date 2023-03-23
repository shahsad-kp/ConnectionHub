from django.urls import path

from .views import admin_report_page, admin_report_handled

urlpatterns = [
    path('', admin_report_page, name='admin-report-page'),
    path('<int:report_id>/handled/', admin_report_handled, name='admin-report-handled'),
]