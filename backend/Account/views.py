import uuid

from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from Account.models import User
from Account.permissions import IsVerified
from Account.serializers import UserSerializer


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UpdateUserView(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsVerified]

    def get_object(self):
        return self.request.user


class CurrentUserView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class VerifyUserEmail(APIView):
    def get(self, request: Request, user_id: uuid, token: str):
        try:
            user = User.objects.get(
                id=user_id
            )
        except User.DoesNotExist:
            return Response(
                data={
                    'message': 'No user found',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if user.is_verified:
            return Response(
                data={
                    'message': 'This email is already verified'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            return Response(
                data={
                    'message': 'Email verified successfully.',
                },
                status=status.HTTP_200_OK
            )
        return Response(
            data={
                'message': 'Token is invalid/expired.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
