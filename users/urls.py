from django.urls import path

from .views import home_view, search_users, follow_user, unfollow_user, settings_update_profile, \
    settings_change_password, settings_delete_account, block_user, unblock_user, send_follow_request, \
    cancel_follow_request, respond_follow_request

urlpatterns = [
    path('search', search_users, name='search-users'),
    path('update/', settings_update_profile, name='update-profile'),
    path('updatepassword', settings_change_password, name='change-password'),
    path('delete/', settings_delete_account, name='delete-profile'),
    path('<str:username>/follow/', follow_user, name='follow-user'),
    path('<str:username>/unfollow/', unfollow_user, name='unfollow-user'),
    path('<str:username>/request/', send_follow_request, name='send-follow-request'),
    path('<str:username>/request/cancel/', cancel_follow_request, name='cancel-follow-request'),
    path('<str:username>/request/<str:action>/', respond_follow_request, name='respond-follow-request'),
    path('<str:username>/block/', block_user, name='block-user'),
    path('<str:username>/unblock/', unblock_user, name='unblock-user'),
    path('<str:username>/', home_view, name='profile-pages'),
]
