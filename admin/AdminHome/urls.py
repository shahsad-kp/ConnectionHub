from django.urls import path

from .views import admin_home, admin_login, admin_logout

urlpatterns = [
    path('', admin_home, name='admin-home'),
    path('login/', admin_login, name='admin-login'),
    path('logout/', admin_logout, name='admin-logout'),
]