from django.urls import path

from .views import admin_users, admin_search_users, admin_profile_pages, admin_profile_delete

urlpatterns = [
    path('', admin_users, name='admin-users'),
    path('search/', admin_search_users, name='admin-search-users'),
    path('<str:username>/', admin_profile_pages, name='admin-profile-pages'),
    path('<str:username>/delete/', admin_profile_delete, name='admin-profile-delete'),
]
