from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from Account.permissions import NotVerified
from Account.serializers import UserSerializer
from Account.tokens import Token


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UpdateUserView(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CurrentUserView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ResendUserEmailVerification(APIView):
    permission_classes = [IsAuthenticated & NotVerified]

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user
        user.send_verification_email()
        return Response(data={}, status=status.HTTP_200_OK)


class VerifyUserEmail(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, **kwargs):
        user = self.get_user()
        user.verify_email()
        serializer = UserSerializer(instance=user)
        return Response(data=serializer.data)

    def get_user(self):
        token = Token(self.kwargs.get('token'))
        token.verify()
        return token.user
