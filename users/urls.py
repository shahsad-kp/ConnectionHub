from django.urls import path

from .views import home_view, search_users, follow_user, unfollow_user, settings_update_profile, \
    settings_change_password, settings_delete_account

urlpatterns = [
    path('search', search_users, name='search-users'),
    path('update/', settings_update_profile, name='update-profile'),
    path('updatepassword', settings_change_password, name='change-password'),
    path('delete/', settings_delete_account, name='delete-profile'),
    path('<str:username>/follow/', follow_user, name='follow-user'),
    path('<str:username>/unfollow/', unfollow_user, name='unfollow-user'),
    path('<str:username>/', home_view, name='profile-pages'),
]
