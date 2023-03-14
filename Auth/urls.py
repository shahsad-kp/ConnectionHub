from django.urls import path

from .views import *

urlpatterns = [
    path('login/', login_view, name='user-login'),
    path('register/', register_view, name='user-register'),
    path('logout/', logout_view, name='user-logout'),
    path('reset-account/', forgot_password_view, name='user-reset-account'),
    path('check_username/', check_username_availability, name='check-username-availability'),
    path('check_email/', check_email_availability, name='check-email-availability'),
    path('send-otp/', send_otp, name='send-otp'),
    path('verify-otp/', verify_otp, name='verify-otp'),
]