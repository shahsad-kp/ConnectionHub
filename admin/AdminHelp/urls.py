from django.urls import path

from Admin.AdminHelp.views import admin_messages_page

urlpatterns = [
    path('', admin_messages_page, name='admin-messages-page'),
]
