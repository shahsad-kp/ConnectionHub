from django.urls import path

from .views import report_user

urlpatterns = [
    path('', report_user, name='report-user')
]
