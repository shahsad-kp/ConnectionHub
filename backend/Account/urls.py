from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, CurrentUserView, VerifyUserEmail, UpdateUserView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register_view'),
    path('me/', CurrentUserView.as_view(), name='get_current_user'),
    path('update/', UpdateUserView.as_view(), name='update_user_details'),
    path('verify/<str:token>/', VerifyUserEmail.as_view(), name='verify_user_email')
]
