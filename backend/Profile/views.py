from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from Account.models import User
from .models import Profile
from .permissions import ProfileAPIPermission
from .serializers import ProfileSerializer


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