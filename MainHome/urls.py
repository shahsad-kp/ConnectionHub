from django.urls import path

from .views import home_view, login_view, register_view, logout_view, send_otp, verify_otp, \
    check_username_availability, check_email_availability

urlpatterns = [
    path('login/', login_view, name='user-login'),
    path('register/', register_view, name='user-register'),
    path('logout/', logout_view, name='user-logout'),
    path('check_username/', check_username_availability, name='check-username-availability'),
    path('check_email/', check_email_availability, name='check-email-availability'),
    path('send-otp/', send_otp, name='send-otp'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    path('', home_view, name='user-home'),
]
