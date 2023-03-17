from django.urls import path

from .views import admin_users, admin_search_users, admin_profile_pages, admin_profile_ban, admin_profile_unban

urlpatterns = [
    path('', admin_users, name='admin-users'),
    path('search/', admin_search_users, name='admin-search-users'),
    path('<str:username>/', admin_profile_pages, name='admin-profile-pages'),
    path('<str:username>/ban/', admin_profile_ban, name='admin-profile-ban'),
    path('<str:username>/unban/', admin_profile_unban, name='admin-profile-unban'),
]