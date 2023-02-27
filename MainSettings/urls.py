from django.urls import path

from .views import settings_home, settings_update_profile, settings_change_password, settings_delete_account, help_view

urlpatterns = [
    path('', settings_home, name='settings-home'),
    path('updateprofile', settings_update_profile, name='profile-settings'),
    path('updatepassword', settings_change_password, name='profile-password'),
    path('deleteaccount', settings_delete_account, name='profile-delete'),
    path('helpcenter', help_view, name='settings-help')
]
