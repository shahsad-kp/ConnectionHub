from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from Account.models import User
from Account.permissions import IsVerified
from .models import Profile
from .permissions import ProfileAPIPermission, ProfileCreatedOnly
from .serializers import ProfileSerializer, FollowSerializer


class ProfileAPIView(RetrieveUpdateAPIView, CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, ProfileAPIPermission]
    queryset = Profile.objects.all()

    def get_object(self) -> Profile:
        user: User = self.request.user
        return get_object_or_404(
            queryset=self.queryset,
            user_id=user.id
        )

    def perform_create(self, serializer: ProfileSerializer):
        serializer.save(user=self.request.user)


class FollowUser(GenericAPIView):
    queryset = Profile.objects.all()
    lookup_url_kwarg = 'profile_id'
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, ProfileCreatedOnly, IsVerified]
    serializer_class = FollowSerializer

    def post(self, request: Request, *_, **__):
        return self.perform_follow(request)

    def perform_follow(self, request):
        followee_profile: Profile = self.get_object()
        serializer: Serializer = self.get_serializer(
            data={'follower': request.user.profile, 'followee': followee_profile}
        )
        serializer.save()
        return Response(
            data=serializer.data
        )
