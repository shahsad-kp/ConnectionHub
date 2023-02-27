from django.urls import path

from .views import home_view, login_view, register_view, logout_view

urlpatterns = [
    path('', home_view, name='user-home'),
    path('login/', login_view, name='user-login'),
    path('register/', register_view, name='user-register'),
    path('logout/', logout_view, name='user-logout'),
]
