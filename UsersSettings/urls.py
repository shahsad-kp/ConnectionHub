from django.urls import path

from .views import privacy_settings, update_user_account_type

urlpatterns = [
    path('privacy/', privacy_settings, name='privacy-settings'),
    path('update-privacy/', update_user_account_type, name='update-acc-type')
]
