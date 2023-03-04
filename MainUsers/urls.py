from django.urls import path

from .views import home_view, search_users, follow_user, unfollow_user, report_user

urlpatterns = [
    path('search', search_users, name='search-users'),
    path('<str:username>/follow/', follow_user, name='follow-user'),
    path('<str:username>/unfollow/', unfollow_user, name='unfollow-user'),
    path('<str:username>/report/', report_user, name='report-user'),
    path('<str:username>', home_view, name='profile-pages'),
]
