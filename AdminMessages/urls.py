from django.urls import path

from .views import admin_messages_page

urlpatterns = [
    path('', admin_messages_page, name='admin_messages_page'),
]
