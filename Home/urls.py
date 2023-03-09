from django.urls import path

from .views import home_view, settings_home

urlpatterns = [
    path('', home_view, name='user-home'),
    path('settings/', settings_home, name='settings-home'),
]
