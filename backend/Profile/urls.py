from django.urls import path

from Profile.views import ProfileAPIView

urlpatterns = [
    path('', ProfileAPIView.as_view(), name='profile-api')
]