from django.urls import path

from .views import report_user

urlpatterns = [
    path('<str:username>/', report_user, name='report-user')
]
